"""create calculation table

Revision ID: 6fe58ef1f5ef
Revises:
Create Date: 2025-02-26 10:07:32.649693

"""

"""create calculation table"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "6fe58ef1f5ef"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "calculations",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("x1", sa.Float, nullable=False),
        sa.Column("x2", sa.Float, nullable=False),
        sa.Column("sum", sa.Float, nullable=False),
    )


def downgrade():
    op.drop_table("calculations")
