"""Add CASCADE for Document

Revision ID: 28e5ba024f67
Revises: b9ae5268f658
Create Date: 2025-06-16 17:06:41.747514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28e5ba024f67'
down_revision: Union[str, None] = 'b9ae5268f658'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('fk_collection_document_document_id_document'), 'collection_document', type_='foreignkey')
    op.create_foreign_key(op.f('fk_collection_document_document_id_document'), 'collection_document', 'document', ['document_id'], ['id'], ondelete='cascade')
    op.drop_constraint(op.f('fk_statistic_document_id_document'), 'statistic', type_='foreignkey')
    op.create_foreign_key(op.f('fk_statistic_document_id_document'), 'statistic', 'document', ['document_id'], ['id'], ondelete='cascade')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('fk_statistic_document_id_document'), 'statistic', type_='foreignkey')
    op.create_foreign_key(op.f('fk_statistic_document_id_document'), 'statistic', 'document', ['document_id'], ['id'])
    op.drop_constraint(op.f('fk_collection_document_document_id_document'), 'collection_document', type_='foreignkey')
    op.create_foreign_key(op.f('fk_collection_document_document_id_document'), 'collection_document', 'document', ['document_id'], ['id'])
