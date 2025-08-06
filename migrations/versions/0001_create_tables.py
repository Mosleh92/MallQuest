"""create users and receipts tables

Revision ID: 0001
Revises: 
Create Date: 2024-06-01
"""

from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('password_hash', sa.String(), nullable=True),
        sa.Column('coins', sa.Integer(), default=0),
        sa.Column('xp', sa.Integer(), default=0),
        sa.Column('level', sa.Integer(), default=1),
        sa.Column('vip_tier', sa.String(), default='Bronze'),
        sa.Column('vip_points', sa.Integer(), default=0),
        sa.Column('total_spent', sa.Float(), default=0.0),
        sa.Column('language', sa.String(), default='en'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'receipts',
        sa.Column('receipt_id', sa.String(), primary_key=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('store', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('items', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('receipts')
    op.drop_table('users')
