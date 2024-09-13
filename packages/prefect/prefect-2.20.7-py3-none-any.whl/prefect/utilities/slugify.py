# Allows prefect to be used side-by-side with unicode-slugify
# See https://github.com/PrefectHQ/prefect/issues/6945

from slugify import slugify

__all__ = ["slugify"]
