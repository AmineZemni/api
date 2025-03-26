"""create files table

Revision ID: 99f548599e03
Revises: 689bfdece488
Create Date: 2025-03-26 17:47:05.743875

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "99f548599e03"
down_revision: Union[str, None] = "689bfdece488"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "file",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "id_user",
            sa.UUID(),
            sa.ForeignKey(
                "user.id", ondelete="CASCADE"
            ),  # Foreign key referencing the user table
            nullable=False,
        ),
        sa.Column(
            "creation_date",
            sa.DateTime(),
            server_default=sa.func.now(),  # Set the default value to the current timestamp
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="file_pkey"),
    )


def downgrade() -> None:
    op.drop_table("file")
