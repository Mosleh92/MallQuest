"""add role column to users

Revision ID: 0002_add_role_to_users
Revises: 0001_create_tables
Create Date: 2024-06-07
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_add_role_to_users'
down_revision = '0001_create_tables'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('role', sa.String(length=20), server_default='player'))


def downgrade():
    op.drop_column('users', 'role')
