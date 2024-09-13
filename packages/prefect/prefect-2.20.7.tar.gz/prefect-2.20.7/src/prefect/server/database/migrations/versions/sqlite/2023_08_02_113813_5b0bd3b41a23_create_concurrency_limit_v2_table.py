"""Create concurrency_limit_v2 table

Revision ID: 5b0bd3b41a23
Revises: 2dbcec43c857
Create Date: 2023-08-02 11:38:13.546075

"""
import sqlalchemy as sa
from alembic import op

import prefect

# revision identifiers, used by Alembic.
revision = "5b0bd3b41a23"
down_revision = "2dbcec43c857"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "concurrency_limit_v2",
        sa.Column(
            "id",
            prefect.server.utilities.database.UUID(),
            server_default=sa.text(
                "(\n    (\n        lower(hex(randomblob(4)))\n        || '-'\n       "
                " || lower(hex(randomblob(2)))\n        || '-4'\n        ||"
                " substr(lower(hex(randomblob(2))),2)\n        || '-'\n        ||"
                " substr('89ab',abs(random()) % 4 + 1, 1)\n        ||"
                " substr(lower(hex(randomblob(2))),2)\n        || '-'\n        ||"
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
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("limit", sa.Integer(), nullable=False),
        sa.Column("active_slots", sa.Integer(), nullable=False),
        sa.Column("denied_slots", sa.Integer(), nullable=False),
        sa.Column("slot_decay_per_second", sa.Float(), nullable=True),
        sa.Column("avg_slot_occupancy_seconds", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_concurrency_limit_v2")),
        sa.UniqueConstraint("name", name=op.f("uq_concurrency_limit_v2__name")),
    )
    with op.batch_alter_table("concurrency_limit_v2", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_concurrency_limit_v2__updated"), ["updated"], unique=False
        )


def downgrade():
    with op.batch_alter_table("concurrency_limit_v2", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_concurrency_limit_v2__updated"))

    op.drop_table("concurrency_limit_v2")
