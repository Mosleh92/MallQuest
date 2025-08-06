"""create wager tables

Revision ID: 0003_create_wager_tables
Revises: 0002_add_role_to_users
Create Date: 2024-06-24
"""

from alembic import op
import sqlalchemy as sa

revision = '0003_create_wager_tables'
down_revision = '0002_add_role_to_users'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'wager_matches',
        sa.Column('match_id', sa.String(), primary_key=True),
        sa.Column('stake', sa.Float(), nullable=True),
        sa.Column('pot', sa.Float(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('map_data', sa.JSON(), nullable=True),
        sa.Column('safe_zones', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_table(
        'wager_players',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('match_id', sa.String(), sa.ForeignKey('wager_matches.match_id')),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('stake', sa.Float(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_table(
        'voucher_catalog',
        sa.Column('voucher_id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('voucher_catalog')
    op.drop_table('wager_players')
    op.drop_table('wager_matches')
