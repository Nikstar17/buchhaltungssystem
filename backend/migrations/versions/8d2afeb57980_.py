"""empty message

Revision ID: 8d2afeb57980
Revises: 9ecc476d2e01
Create Date: 2025-04-06 11:41:54.682810

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8d2afeb57980'
down_revision = '9ecc476d2e01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('uploads', schema=None) as batch_op:
        batch_op.alter_column('file_data',
               existing_type=postgresql.BYTEA(),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('uploads', schema=None) as batch_op:
        batch_op.alter_column('file_data',
               existing_type=sa.Text(),
               type_=postgresql.BYTEA(),
               existing_nullable=True)

    # ### end Alembic commands ###
