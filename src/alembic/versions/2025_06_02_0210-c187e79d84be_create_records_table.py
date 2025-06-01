"""create records table

Revision ID: c187e79d84be
Revises:
Create Date: 2025-06-02 02:10:31.375217

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c187e79d84be"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "records",
        sa.Column(
            "latest_file_processed_timestamp", sa.TIMESTAMP(), nullable=True
        ),
        sa.Column("files_processed", sa.Integer(), nullable=False),
        sa.Column("min_time_processed", sa.Float(), nullable=False),
        sa.Column("avg_time_processed", sa.Float(), nullable=False),
        sa.Column("max_time_processed", sa.Float(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_records")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("records")
