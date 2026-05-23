"""add username column to post

Revision ID: 3f1a2b4c5d6e
Revises: 2c0f7e89f84a
Create Date: 2026-05-23 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f1a2b4c5d6e'
down_revision = '2c0f7e89f84a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=50), nullable=False, server_default='unknown'))


def downgrade():
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('username')