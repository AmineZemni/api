"""create users table

Revision ID: 689bfdece488
Revises:
Create Date: 2025-03-25 03:30:13.661387

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "689bfdece488"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "key",
            sa.String(),
            autoincrement=False,
            nullable=False,
            unique=True,
        ),
        sa.PrimaryKeyConstraint("id", name="user_pkey"),
    )


def downgrade() -> None:
    op.drop_table("user")
