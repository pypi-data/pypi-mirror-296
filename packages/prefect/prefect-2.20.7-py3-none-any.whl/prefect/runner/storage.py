import shutil
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional, Protocol, TypedDict, Union, runtime_checkable
from urllib.parse import urlparse, urlsplit, urlunparse
from uuid import uuid4

import fsspec
from anyio import run_process

from prefect._internal.concurrency.api import create_call, from_async
from prefect._internal.pydantic import HAS_PYDANTIC_V2
from prefect.blocks.core import Block, BlockNotSavedError
from prefect.blocks.system import Secret
from prefect.filesystems import ReadableDeploymentStorage, WritableDeploymentStorage
from prefect.logging.loggers import get_logger
from prefect.utilities.collections import visit_collection

if HAS_PYDANTIC_V2:
    from pydantic.v1 import SecretStr
else:
    from pydantic import SecretStr


@runtime_checkable
class RunnerStorage(Protocol):
    """
    A storage interface for a runner to use to retrieve
    remotely stored flow code.
    """

    def set_base_path(self, path: Path):
        """
        Sets the base path to use when pulling contents from remote storage to
        local storage.
        """
        ...

    @property
    def pull_interval(self) -> Optional[int]:
        """
        The interval at which contents from remote storage should be pulled to
        local storage. If None, remote storage will perform a one-time sync.
        """
        ...

    @property
    def destination(self) -> Path:
        """
        The local file path to pull contents from remote storage to.
        """
        ...

    async def pull_code(self):
        """
        Pulls contents from remote storage to the local filesystem.
        """
        ...

    def to_pull_step(self) -> dict:
        """
        Returns a dictionary representation of the storage object that can be
        used as a deployment pull step.
        """
        ...

    def __eq__(self, __value) -> bool:
        """
        Equality check for runner storage objects.
        """
        ...


class GitCredentials(TypedDict, total=False):
    username: str
    access_token: Union[str, Secret]


class GitRepository:
    """
    Pulls the contents of a git repository to the local filesystem.

    Parameters:
        url: The URL of the git repository to pull from
        credentials: A dictionary of credentials to use when pulling from the
            repository. If a username is provided, an access token must also be
            provided.
        name: The name of the repository. If not provided, the name will be
            inferred from the repository URL.
        branch: The branch to pull from. Defaults to "main".
        pull_interval: The interval in seconds at which to pull contents from
            remote storage to local storage. If None, remote storage will perform
            a one-time sync.

    Examples:
        Pull the contents of a private git repository to the local filesystem:

        ```python
        from prefect.runner.storage import GitRepository

        storage = GitRepository(
            url="https://github.com/org/repo.git",
            credentials={"username": "oauth2", "access_token": "my-access-token"},
        )

        await storage.pull_code()
        ```
    """

    def __init__(
        self,
        url: str,
        credentials: Union[GitCredentials, Block, Dict[str, Any], None] = None,
        name: Optional[str] = None,
        branch: Optional[str] = None,
        include_submodules: bool = False,
        pull_interval: Optional[int] = 60,
    ):
        if credentials is None:
            credentials = {}

        if (
            isinstance(credentials, dict)
            and credentials.get("username")
            and not (credentials.get("access_token") or credentials.get("password"))
        ):
            raise ValueError(
                "If a username is provided, an access token or password must also be"
                " provided."
            )
        self._url = url
        self._branch = branch
        self._credentials = credentials
        self._include_submodules = include_submodules
        repo_name = urlparse(url).path.split("/")[-1].replace(".git", "")
        default_name = f"{repo_name}-{branch}" if branch else repo_name
        self._name = name or default_name
        self._logger = get_logger(f"runner.storage.git-repository.{self._name}")
        self._storage_base_path = Path.cwd()
        self._pull_interval = pull_interval

    @property
    def destination(self) -> Path:
        return self._storage_base_path / self._name

    def set_base_path(self, path: Path):
        self._storage_base_path = path

    @property
    def pull_interval(self) -> Optional[int]:
        return self._pull_interval

    @property
    def _repository_url_with_credentials(self) -> str:
        if not self._credentials:
            return self._url

        url_components = urlparse(self._url)

        credentials = (
            self._credentials.dict()
            if isinstance(self._credentials, Block)
            else deepcopy(self._credentials)
        )

        for k, v in credentials.items():
            if isinstance(v, Secret):
                credentials[k] = v.get()
            elif isinstance(v, SecretStr):
                credentials[k] = v.get_secret_value()

        formatted_credentials = _format_token_from_credentials(
            urlparse(self._url).netloc, credentials
        )
        if url_components.scheme == "https" and formatted_credentials is not None:
            updated_components = url_components._replace(
                netloc=f"{formatted_credentials}@{url_components.netloc}"
            )
            repository_url = urlunparse(updated_components)
        else:
            repository_url = self._url

        return repository_url

    async def pull_code(self):
        """
        Pulls the contents of the configured repository to the local filesystem.
        """
        self._logger.debug(
            "Pulling contents from repository '%s' to '%s'...",
            self._name,
            self.destination,
        )

        git_dir = self.destination / ".git"

        if git_dir.exists():
            # Check if the existing repository matches the configured repository
            result = await run_process(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=str(self.destination),
            )
            existing_repo_url = None
            if result.stdout is not None:
                existing_repo_url = _strip_auth_from_url(result.stdout.decode().strip())

            if existing_repo_url != self._url:
                raise ValueError(
                    f"The existing repository at {str(self.destination)} "
                    f"does not match the configured repository {self._url}"
                )

            self._logger.debug("Pulling latest changes from origin/%s", self._branch)
            # Update the existing repository
            cmd = ["git", "pull", "origin"]
            if self._branch:
                cmd += [self._branch]
            if self._include_submodules:
                cmd += ["--recurse-submodules"]
            cmd += ["--depth", "1"]
            try:
                await run_process(cmd, cwd=self.destination)
                self._logger.debug("Successfully pulled latest changes")
            except subprocess.CalledProcessError as exc:
                self._logger.error(
                    f"Failed to pull latest changes with exit code {exc}"
                )
                shutil.rmtree(self.destination)
                await self._clone_repo()

        else:
            await self._clone_repo()

    async def _clone_repo(self):
        """
        Clones the repository into the local destination.
        """
        self._logger.debug("Cloning repository %s", self._url)

        repository_url = self._repository_url_with_credentials

        cmd = [
            "git",
            "clone",
            repository_url,
        ]
        if self._branch:
            cmd += ["--branch", self._branch]
        if self._include_submodules:
            cmd += ["--recurse-submodules"]

        # Limit git history and set path to clone to
        cmd += ["--depth", "1", str(self.destination)]

        try:
            await run_process(cmd)
        except subprocess.CalledProcessError as exc:
            # Hide the command used to avoid leaking the access token
            exc_chain = None if self._credentials else exc
            raise RuntimeError(
                f"Failed to clone repository {self._url!r} with exit code"
                f" {exc.returncode}."
            ) from exc_chain

    def __eq__(self, __value) -> bool:
        if isinstance(__value, GitRepository):
            return (
                self._url == __value._url
                and self._branch == __value._branch
                and self._name == __value._name
            )
        return False

    def __repr__(self) -> str:
        return (
            f"GitRepository(name={self._name!r} repository={self._url!r},"
            f" branch={self._branch!r})"
        )

    def to_pull_step(self) -> Dict:
        pull_step = {
            "prefect.deployments.steps.git_clone": {
                "repository": self._url,
                "branch": self._branch,
            }
        }
        if self._include_submodules:
            pull_step["prefect.deployments.steps.git_clone"][
                "include_submodules"
            ] = self._include_submodules
        if isinstance(self._credentials, Block):
            pull_step["prefect.deployments.steps.git_clone"][
                "credentials"
            ] = f"{{{{ {self._credentials.get_block_placeholder()} }}}}"
        elif isinstance(self._credentials, dict):
            if isinstance(self._credentials.get("access_token"), Secret):
                pull_step["prefect.deployments.steps.git_clone"]["credentials"] = {
                    **self._credentials,
                    "access_token": (
                        "{{"
                        f" {self._credentials['access_token'].get_block_placeholder()} }}}}"
                    ),
                }
            elif self._credentials.get("access_token") is not None:
                raise ValueError(
                    "Please save your access token as a Secret block before converting"
                    " this storage object to a pull step."
                )

        return pull_step


class RemoteStorage:
    """
    Pulls the contents of a remote storage location to the local filesystem.

    Parameters:
        url: The URL of the remote storage location to pull from. Supports
            `fsspec` URLs. Some protocols may require an additional `fsspec`
            dependency to be installed. Refer to the
            [`fsspec` docs](https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations)
            for more details.
        pull_interval: The interval in seconds at which to pull contents from
            remote storage to local storage. If None, remote storage will perform
            a one-time sync.
        **settings: Any additional settings to pass the `fsspec` filesystem class.

    Examples:
        Pull the contents of a remote storage location to the local filesystem:

        ```python
        from prefect.runner.storage import RemoteStorage

        storage = RemoteStorage(url="s3://my-bucket/my-folder")

        await storage.pull_code()
        ```

        Pull the contents of a remote storage location to the local filesystem
        with additional settings:

        ```python
        from prefect.runner.storage import RemoteStorage
        from prefect.blocks.system import Secret

        storage = RemoteStorage(
            url="s3://my-bucket/my-folder",
            # Use Secret blocks to keep credentials out of your code
            key=Secret.load("my-aws-access-key"),
            secret=Secret.load("my-aws-secret-key"),
        )

        await storage.pull_code()
        ```
    """

    def __init__(
        self,
        url: str,
        pull_interval: Optional[int] = 60,
        **settings: Any,
    ):
        self._url = url
        self._settings = settings
        self._logger = get_logger("runner.storage.remote-storage")
        self._storage_base_path = Path.cwd()
        self._pull_interval = pull_interval

    @staticmethod
    def _get_required_package_for_scheme(scheme: str) -> Optional[str]:
        # attempt to discover the package name for the given scheme
        # from fsspec's registry
        known_implementation = fsspec.registry.get(scheme)
        if known_implementation:
            return known_implementation.__module__.split(".")[0]
        # if we don't know the implementation, try to guess it for some
        # common schemes
        elif scheme == "s3":
            return "s3fs"
        elif scheme == "gs" or scheme == "gcs":
            return "gcsfs"
        elif scheme == "abfs" or scheme == "az":
            return "adlfs"
        else:
            return None

    @property
    def _filesystem(self) -> fsspec.AbstractFileSystem:
        scheme, _, _, _, _ = urlsplit(self._url)

        def replace_blocks_with_values(obj: Any) -> Any:
            if isinstance(obj, Block):
                if hasattr(obj, "get"):
                    return obj.get()
                if hasattr(obj, "value"):
                    return obj.value
                else:
                    return obj.dict()
            return obj

        settings_with_block_values = visit_collection(
            self._settings, replace_blocks_with_values, return_data=True
        )

        return fsspec.filesystem(scheme, **settings_with_block_values)

    def set_base_path(self, path: Path):
        self._storage_base_path = path

    @property
    def pull_interval(self) -> Optional[int]:
        """
        The interval at which contents from remote storage should be pulled to
        local storage. If None, remote storage will perform a one-time sync.
        """
        return self._pull_interval

    @property
    def destination(self) -> Path:
        """
        The local file path to pull contents from remote storage to.
        """
        return self._storage_base_path / self._remote_path

    @property
    def _remote_path(self) -> Path:
        """
        The remote file path to pull contents from remote storage to.
        """
        _, netloc, urlpath, _, _ = urlsplit(self._url)
        return Path(netloc) / Path(urlpath.lstrip("/"))

    async def pull_code(self):
        """
        Pulls contents from remote storage to the local filesystem.
        """
        self._logger.debug(
            "Pulling contents from remote storage '%s' to '%s'...",
            self._url,
            self.destination,
        )

        if not self.destination.exists():
            self.destination.mkdir(parents=True, exist_ok=True)

        remote_path = str(self._remote_path) + "/"

        try:
            await from_async.wait_for_call_in_new_thread(
                create_call(
                    self._filesystem.get,
                    remote_path,
                    str(self.destination),
                    recursive=True,
                )
            )
        except Exception as exc:
            raise RuntimeError(
                f"Failed to pull contents from remote storage {self._url!r} to"
                f" {self.destination!r}"
            ) from exc

    def to_pull_step(self) -> dict:
        """
        Returns a dictionary representation of the storage object that can be
        used as a deployment pull step.
        """

        def replace_block_with_placeholder(obj: Any) -> Any:
            if isinstance(obj, Block):
                return f"{{{{ {obj.get_block_placeholder()} }}}}"
            return obj

        settings_with_placeholders = visit_collection(
            self._settings, replace_block_with_placeholder, return_data=True
        )
        required_package = self._get_required_package_for_scheme(
            urlparse(self._url).scheme
        )
        step = {
            "prefect.deployments.steps.pull_from_remote_storage": {
                "url": self._url,
                **settings_with_placeholders,
            }
        }
        if required_package:
            step["prefect.deployments.steps.pull_from_remote_storage"][
                "requires"
            ] = required_package
        return step

    def __eq__(self, __value) -> bool:
        """
        Equality check for runner storage objects.
        """
        if isinstance(__value, RemoteStorage):
            return self._url == __value._url and self._settings == __value._settings
        return False

    def __repr__(self) -> str:
        return f"RemoteStorage(url={self._url!r})"


class BlockStorageAdapter:
    """
    A storage adapter for a storage block object to allow it to be used as a
    runner storage object.
    """

    def __init__(
        self,
        block: Union[ReadableDeploymentStorage, WritableDeploymentStorage],
        pull_interval: Optional[int] = 60,
    ):
        self._block = block
        self._pull_interval = pull_interval
        self._storage_base_path = Path.cwd()
        if not isinstance(block, Block):
            raise TypeError(
                f"Expected a block object. Received a {type(block).__name__!r} object."
            )
        if not hasattr(block, "get_directory"):
            raise ValueError("Provided block must have a `get_directory` method.")

        self._name = (
            f"{block.get_block_type_slug()}-{block._block_document_name}"
            if block._block_document_name
            else str(uuid4())
        )

    def set_base_path(self, path: Path):
        self._storage_base_path = path

    @property
    def pull_interval(self) -> Optional[int]:
        return self._pull_interval

    @property
    def destination(self) -> Path:
        return self._storage_base_path / self._name

    async def pull_code(self):
        if not self.destination.exists():
            self.destination.mkdir(parents=True, exist_ok=True)
        await self._block.get_directory(local_path=str(self.destination))

    def to_pull_step(self) -> dict:
        # Give blocks the change to implement their own pull step
        if hasattr(self._block, "get_pull_step"):
            return self._block.get_pull_step()
        else:
            if not self._block._block_document_name:
                raise BlockNotSavedError(
                    "Block must be saved with `.save()` before it can be converted to a"
                    " pull step."
                )
            return {
                "prefect.deployments.steps.pull_with_block": {
                    "block_type_slug": self._block.get_block_type_slug(),
                    "block_document_name": self._block._block_document_name,
                }
            }

    def __eq__(self, __value) -> bool:
        if isinstance(__value, BlockStorageAdapter):
            return self._block == __value._block
        return False


class LocalStorage:
    """
    Sets the working directory in the local filesystem.

    Parameters:
        Path: Local file path to set the working directory for the flow

    Examples:
        Sets the working directory for the local path to the flow:

        ```python
        from prefect.runner.storage import Localstorage

        storage = LocalStorage(
            path="/path/to/local/flow_directory",
        )
        ```
    """

    def __init__(
        self,
        path: str,
        pull_interval: Optional[int] = None,
    ):
        self._path = Path(path).resolve()
        self._logger = get_logger("runner.storage.local-storage")
        self._storage_base_path = Path.cwd()
        self._pull_interval = pull_interval

    @property
    def destination(self) -> Path:
        return self._path

    def set_base_path(self, path: Path):
        self._storage_base_path = path

    @property
    def pull_interval(self) -> Optional[int]:
        return self._pull_interval

    async def pull_code(self):
        # Local storage assumes the code already exists on the local filesystem
        # and does not need to be pulled from a remote location
        pass

    def to_pull_step(self) -> dict:
        """
        Returns a dictionary representation of the storage object that can be
        used as a deployment pull step.
        """
        step = {
            "prefect.deployments.steps.set_working_directory": {
                "directory": str(self.destination)
            }
        }
        return step

    def __eq__(self, __value) -> bool:
        if isinstance(__value, LocalStorage):
            return self._path == __value._path
        return False

    def __repr__(self) -> str:
        return f"LocalStorage(path={self._path!r})"


def create_storage_from_source(
    source: str, pull_interval: Optional[int] = 60
) -> RunnerStorage:
    """
    Creates a storage object from a URL.

    Args:
        url: The URL to create a storage object from. Supports git and `fsspec`
            URLs.
        pull_interval: The interval at which to pull contents from remote storage to
            local storage

    Returns:
        RunnerStorage: A runner storage compatible object
    """
    logger = get_logger("runner.storage")
    parsed_source = urlparse(source)
    if parsed_source.scheme == "git" or parsed_source.path.endswith(".git"):
        return GitRepository(url=source, pull_interval=pull_interval)
    elif parsed_source.scheme in ("file", "local"):
        source_path = source.split("://", 1)[-1]
        return LocalStorage(path=source_path, pull_interval=pull_interval)
    elif parsed_source.scheme in fsspec.available_protocols():
        return RemoteStorage(url=source, pull_interval=pull_interval)
    else:
        logger.debug("No valid fsspec protocol found for URL, assuming local storage.")
        return LocalStorage(path=source, pull_interval=pull_interval)


def _format_token_from_credentials(netloc: str, credentials: dict) -> str:
    """
    Formats the credentials block for the git provider.

    BitBucket supports the following syntax:
        git clone "https://x-token-auth:{token}@bitbucket.org/yourRepoOwnerHere/RepoNameHere"
        git clone https://username:<token>@bitbucketserver.com/scm/projectname/teamsinspace.git
    """
    username = credentials.get("username") if credentials else None
    password = credentials.get("password") if credentials else None
    token = credentials.get("token") if credentials else None
    access_token = credentials.get("access_token") if credentials else None

    user_provided_token = access_token or token or password

    if not user_provided_token:
        raise ValueError(
            "Please provide a `token` or `password` in your Credentials block to clone"
            " a repo."
        )

    if username:
        return f"{username}:{user_provided_token}"

    if "bitbucketserver" in netloc:
        # If they pass a BitBucketCredentials block and we don't have both a username and at
        # least one of a password or token and they don't provide a header themselves,
        # we can raise the appropriate error to avoid the wrong format for BitBucket Server.
        if not username and ":" not in user_provided_token:
            raise ValueError(
                "Please provide a `username` and a `password` or `token` in your"
                " BitBucketCredentials block to clone a repo from BitBucket Server."
            )
        # if username or if no username but it's provided in the token
        return (
            f"{username}:{user_provided_token}"
            if username and username not in user_provided_token
            else user_provided_token
        )

    elif "bitbucket" in netloc:
        return (
            user_provided_token
            if user_provided_token.startswith("x-token-auth:")
            or ":" in user_provided_token
            else f"x-token-auth:{user_provided_token}"
        )

    elif "gitlab" in netloc:
        return (
            f"oauth2:{user_provided_token}"
            if not user_provided_token.startswith("oauth2:")
            else user_provided_token
        )

    # all other cases (GitHub, etc.)
    return user_provided_token


def _strip_auth_from_url(url: str) -> str:
    parsed = urlparse(url)

    # Construct a new netloc without the auth info
    netloc = parsed.hostname
    if parsed.port:
        netloc += f":{parsed.port}"

    # Build the sanitized URL
    return urlunparse(
        (
            parsed.scheme,
            netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )
