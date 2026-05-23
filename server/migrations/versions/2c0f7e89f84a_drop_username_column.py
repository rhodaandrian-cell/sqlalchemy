"""drop username column

Revision ID: 2c0f7e89f84a
Revises: 2400b5c601a5
Create Date: 2026-05-07 20:00:00.829621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c0f7e89f84a'
down_revision = '2400b5c601a5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('username')


def downgrade():
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=50), nullable=False))