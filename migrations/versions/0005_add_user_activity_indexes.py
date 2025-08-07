"""add indexes for user activity columns"""

from alembic import op
import sqlalchemy as sa

revision = '0005_add_user_activity_indexes'
down_revision = '0004_add_mall_entry_and_last_entry_at'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('ix_users_last_entry_at', 'users', ['last_entry_at'])
    op.create_index('ix_users_last_purchase_at', 'users', ['last_purchase_at'])


def downgrade():
    op.drop_index('ix_users_last_purchase_at', table_name='users')
    op.drop_index('ix_users_last_entry_at', table_name='users')
