"""add fk posts_users

Revision ID: 6716f73ff2c5
Revises: f341d2a4f71d
Create Date: 2022-10-04 16:33:52.709159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6716f73ff2c5'
down_revision = 'f341d2a4f71d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer, nullable=False))
    op.create_foreign_key('fk_posts_users',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('fk_posts_users', table_name="posts")
    op.drop_column('posts','owner_id')
    pass
