"""create post table

Revision ID: 431a45bf0d9f
Revises: 
Create Date: 2022-10-04 15:04:07.705738

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import INTEGER, VARCHAR, String, Boolean,TIMESTAMP, Column
from sqlalchemy.sql import text
from alembic import op

# revision identifiers, used by Alembic.
revision = '431a45bf0d9f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        Column("id", INTEGER, nullable=False, primary_key=True),
        Column("title", VARCHAR(255), nullable=False),
        Column("content", String(255), nullable=False),
        Column("published", Boolean, default=True, nullable=False),
        Column("create_at", TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
