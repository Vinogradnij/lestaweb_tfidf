"""Add CASCADE for User

Revision ID: b9ae5268f658
Revises: f785f578ee27
Create Date: 2025-06-16 17:05:14.694490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9ae5268f658'
down_revision: Union[str, None] = 'f785f578ee27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('fk_collection_user_id_user'), 'collection', type_='foreignkey')
    op.create_foreign_key(op.f('fk_collection_user_id_user'), 'collection', 'user', ['user_id'], ['id'], ondelete='cascade')
    op.drop_constraint(op.f('fk_document_user_id_user'), 'document', type_='foreignkey')
    op.create_foreign_key(op.f('fk_document_user_id_user'), 'document', 'user', ['user_id'], ['id'], ondelete='cascade')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('fk_document_user_id_user'), 'document', type_='foreignkey')
    op.create_foreign_key(op.f('fk_document_user_id_user'), 'document', 'user', ['user_id'], ['id'])
    op.drop_constraint(op.f('fk_collection_user_id_user'), 'collection', type_='foreignkey')
    op.create_foreign_key(op.f('fk_collection_user_id_user'), 'collection', 'user', ['user_id'], ['id'])
