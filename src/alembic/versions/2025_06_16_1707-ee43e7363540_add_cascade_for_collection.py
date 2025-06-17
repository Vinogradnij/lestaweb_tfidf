"""Add CASCADE for Collection

Revision ID: ee43e7363540
Revises: 28e5ba024f67
Create Date: 2025-06-16 17:07:58.890676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee43e7363540'
down_revision: Union[str, None] = '28e5ba024f67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('fk_collection_document_collection_id_collection'), 'collection_document', type_='foreignkey')
    op.create_foreign_key(op.f('fk_collection_document_collection_id_collection'), 'collection_document', 'collection', ['collection_id'], ['id'], ondelete='cascade')
    op.drop_constraint(op.f('fk_statistic_collection_id_collection'), 'statistic', type_='foreignkey')
    op.create_foreign_key(op.f('fk_statistic_collection_id_collection'), 'statistic', 'collection', ['collection_id'], ['id'], ondelete='cascade')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('fk_statistic_collection_id_collection'), 'statistic', type_='foreignkey')
    op.create_foreign_key(op.f('fk_statistic_collection_id_collection'), 'statistic', 'collection', ['collection_id'], ['id'])
    op.drop_constraint(op.f('fk_collection_document_collection_id_collection'), 'collection_document', type_='foreignkey')
    op.create_foreign_key(op.f('fk_collection_document_collection_id_collection'), 'collection_document', 'collection', ['collection_id'], ['id'])
