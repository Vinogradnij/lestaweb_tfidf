"""Add unique constraint for Collection_Document

Revision ID: 9a5836248f81
Revises: ebceab1af273
Create Date: 2025-06-16 15:03:39.085493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a5836248f81'
down_revision: Union[str, None] = 'ebceab1af273'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('unique_document_collection', 'collection_document', ['document_id', 'collection_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('unique_document_collection', 'collection_document', type_='unique')
