"""add not null for records.latest_file_processed_timestamp

Revision ID: 69976685e2d1
Revises: 6044954aa2c2
Create Date: 2025-06-02 03:12:29.735616

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "69976685e2d1"
down_revision: Union[str, None] = "6044954aa2c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "records",
        "latest_file_processed_timestamp",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "records",
        "latest_file_processed_timestamp",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
    )
