"""Add unique constraint for Statistic

Revision ID: f785f578ee27
Revises: 9a5836248f81
Create Date: 2025-06-16 15:07:37.797615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f785f578ee27'
down_revision: Union[str, None] = '9a5836248f81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('unique_document_collection_word', 'statistic', ['document_id', 'collection_id', 'word'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('unique_document_collection_word', 'statistic', type_='unique')
