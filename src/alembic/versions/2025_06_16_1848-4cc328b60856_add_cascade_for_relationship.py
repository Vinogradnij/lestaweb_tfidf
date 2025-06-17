"""Add CASCADE for relationship

Revision ID: 4cc328b60856
Revises: ee43e7363540
Create Date: 2025-06-16 18:48:19.897630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cc328b60856'
down_revision: Union[str, None] = 'ee43e7363540'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
