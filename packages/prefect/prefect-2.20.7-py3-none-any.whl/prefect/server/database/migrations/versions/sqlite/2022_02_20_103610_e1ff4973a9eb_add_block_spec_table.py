"""Add block_spec table

Revision ID: e1ff4973a9eb
Revises: 4c4a6a138053
Create Date: 2022-02-20 10:36:10.457956

"""
import sqlalchemy as sa
from alembic import op

import prefect

# revision identifiers, used by Alembic.
revision = "e1ff4973a9eb"
down_revision = "4c4a6a138053"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "block_spec",
        sa.Column(
            "id",
            prefect.server.utilities.database.UUID(),
            server_default=sa.text(
                "(\n    (\n        lower(hex(randomblob(4))) \n        || '-' \n       "
                " || lower(hex(randomblob(2))) \n        || '-4' \n        ||"
                " substr(lower(hex(randomblob(2))),2) \n        || '-' \n        ||"
                " substr('89ab',abs(random()) % 4 + 1, 1) \n        ||"
                " substr(lower(hex(randomblob(2))),2) \n        || '-' \n        ||"
                " lower(hex(randomblob(6)))\n    )\n    )"
            ),
            nullable=False,
        ),
        sa.Column(
            "created",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("(strftime('%Y-%m-%d %H:%M:%f000', 'now'))"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("(strftime('%Y-%m-%d %H:%M:%f000', 'now'))"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column(
            "fields",
            prefect.server.utilities.database.JSON(astext_type=sa.Text()),
            server_default="{}",
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_block_spec")),
    )
    with op.batch_alter_table("block_spec", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_block_spec__updated"), ["updated"], unique=False
        )
        batch_op.create_index(
            "uq_block_spec__name_version", ["name", "version"], unique=True
        )
        batch_op.create_index(batch_op.f("ix_block_spec__type"), ["type"], unique=False)

    with op.batch_alter_table("block", schema=None) as batch_op:
        batch_op.drop_index("ix_block_data__name")
        batch_op.drop_index("ix_block_data__updated")
        batch_op.create_index(batch_op.f("ix_block__name"), ["name"], unique=False)
        batch_op.create_index(
            batch_op.f("ix_block__updated"), ["updated"], unique=False
        )
        batch_op.create_unique_constraint(batch_op.f("uq_block__name"), ["name"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("block", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("uq_block__name"), type_="unique")
        batch_op.drop_index(batch_op.f("ix_block__updated"))
        batch_op.drop_index(batch_op.f("ix_block__name"))
        batch_op.create_index("ix_block_data__updated", ["updated"], unique=False)
        batch_op.create_index("ix_block_data__name", ["name"], unique=False)

    with op.batch_alter_table("block_spec", schema=None) as batch_op:
        batch_op.drop_index("uq_block_spec__name_version")
        batch_op.drop_index(batch_op.f("ix_block_spec__updated"))
        batch_op.drop_index(batch_op.f("ix_block_spec__type"))

    op.drop_table("block_spec")
    # ### end Alembic commands ###
