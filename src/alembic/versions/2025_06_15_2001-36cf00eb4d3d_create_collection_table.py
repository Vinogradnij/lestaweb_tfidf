"""Create Collection table

Revision ID: 36cf00eb4d3d
Revises: 2d4e96d20067
Create Date: 2025-06-15 20:01:41.253887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36cf00eb4d3d'
down_revision: Union[str, None] = '2d4e96d20067'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('collection',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_collection_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_collection'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('collection')
