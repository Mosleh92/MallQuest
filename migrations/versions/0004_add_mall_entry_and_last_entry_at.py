"""add mall entry table and last_entry_at column

Revision ID: 0004_add_mall_entry_and_last_entry_at
Revises: 0003_create_wager_tables
Create Date: 2024-07-05
"""

from alembic import op
import sqlalchemy as sa


revision = '0004_add_mall_entry_and_last_entry_at'
down_revision = '0003_create_wager_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mall_entries',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('device_info', sa.JSON(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
    )
    op.add_column('users', sa.Column('last_entry_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('users', 'last_entry_at')
    op.drop_table('mall_entries')

