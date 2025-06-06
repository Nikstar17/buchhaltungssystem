"""empty message

Revision ID: 8f0f74976462
Revises: 1ae49c2a8c55
Create Date: 2025-04-10 15:22:34.919114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f0f74976462'
down_revision = '1ae49c2a8c55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_chart_of_account_settings',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('account_id', sa.UUID(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('custom_name', sa.String(), nullable=True),
    sa.Column('custom_description', sa.Text(), nullable=True),
    sa.Column('favorite', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'account_id', name='uix_user_chart_account')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_chart_of_account_settings')
    # ### end Alembic commands ###
