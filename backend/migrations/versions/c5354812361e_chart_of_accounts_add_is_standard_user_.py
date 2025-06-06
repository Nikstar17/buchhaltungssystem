"""chart_of_accounts add is_standard + user_id nullable=true

Revision ID: c5354812361e
Revises: 92ab986af0ef
Create Date: 2025-04-03 13:10:10.467410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5354812361e'
down_revision = '92ab986af0ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chart_of_accounts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_standard', sa.Boolean(), nullable=False))
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chart_of_accounts', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               nullable=False)
        batch_op.drop_column('is_standard')

    # ### end Alembic commands ###
