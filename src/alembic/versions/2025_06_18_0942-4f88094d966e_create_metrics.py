"""Create Metrics

Revision ID: 4f88094d966e
Revises: 4cc328b60856
Create Date: 2025-06-18 09:42:31.395697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f88094d966e'
down_revision: Union[str, None] = '4cc328b60856'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('metrics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('files_processed', sa.Integer(), nullable=False),
    sa.Column('min_time_processed', sa.Float(), nullable=False),
    sa.Column('avg_time_processed', sa.Float(), nullable=False),
    sa.Column('max_time_processed', sa.Float(), nullable=False),
    sa.Column('all_time_processed', sa.Float(), nullable=False),
    sa.Column('latest_file_processed_timestamp', sa.Float(), nullable=False),
    sa.Column('files_huffman', sa.Integer(), nullable=False),
    sa.Column('min_time_huffman', sa.Float(), nullable=False),
    sa.Column('avg_time_huffman', sa.Float(), nullable=False),
    sa.Column('max_time_huffman', sa.Float(), nullable=False),
    sa.Column('all_time_huffman', sa.Float(), nullable=False),
    sa.Column('latest_huffman', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_metrics'))
    )
    op.execute('''
            INSERT INTO metrics (
                files_processed,
                min_time_processed,
                avg_time_processed,
                max_time_processed,
                all_time_processed,
                latest_file_processed_timestamp,
                files_huffman,
                min_time_huffman,
                avg_time_huffman,
                max_time_huffman,
                all_time_huffman,
                latest_huffman
            )
            VALUES (
                0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0
            )
        ''')

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('metrics')
