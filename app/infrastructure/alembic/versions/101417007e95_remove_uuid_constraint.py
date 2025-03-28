"""change id and id_user types to UUID in file and user tables

Revision ID: a1b2c3d4e5f6
Revises: 99f548599e03
Create Date: 2025-03-28 12:00:00.000000
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "99f548599e03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("file_id_user_fkey", "file", type_="foreignkey")

    # 2. Change column types to VARCHAR(255)
    op.alter_column(
        "user", "id", type_=sa.String(length=255), postgresql_using="id::varchar(255)"
    )
    op.alter_column(
        "file", "id", type_=sa.String(length=255), postgresql_using="id::varchar(255)"
    )
    op.alter_column(
        "file",
        "id_user",
        type_=sa.String(length=255),
        postgresql_using="id_user::varchar(255)",
    )

    # 3. Recreate the FK constraint with matching types
    op.create_foreign_key(
        "file_id_user_fkey", "file", "user", ["id_user"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    # 1. Drop FK before reverting types
    op.drop_constraint("file_id_user_fkey", "file", type_="foreignkey")

    # 2. Revert to UUID
    op.alter_column(
        "file", "id_user", type_=sa.UUID(), postgresql_using="id_user::uuid"
    )
    op.alter_column("file", "id", type_=sa.UUID(), postgresql_using="id::uuid")
    op.alter_column("user", "id", type_=sa.UUID(), postgresql_using="id::uuid")

    # 3. Recreate FK
    op.create_foreign_key(
        "file_id_user_fkey", "file", "user", ["id_user"], ["id"], ondelete="CASCADE"
    )
