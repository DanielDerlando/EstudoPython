"""create users table

Revision ID: f341d2a4f71d
Revises: 431a45bf0d9f
Create Date: 2022-10-04 16:06:53.449067

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column,Integer,String,TIMESTAMP


# revision identifiers, used by Alembic.
revision = 'f341d2a4f71d'
down_revision = '431a45bf0d9f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        Column('id',Integer,primary_key=True, nullable=False),
        Column('name',String(255), nullable=False),
        Column('email',String(255), nullable=False, unique=True),
        Column('password',String(255), nullable=False),
        Column('created_at',TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email') 
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
