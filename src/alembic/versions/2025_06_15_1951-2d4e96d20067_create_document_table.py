"""Create Document table

Revision ID: 2d4e96d20067
Revises: eb9898bdc438
Create Date: 2025-06-15 19:51:18.635862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d4e96d20067'
down_revision: Union[str, None] = 'eb9898bdc438'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('document',
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_document_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_document'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('document')
