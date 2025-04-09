"""add_account_explanations_table

Revision ID: 91b6b8e5a96b
Revises: f83294852080
Create Date: 2025-04-08 10:47:05.534545

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '91b6b8e5a96b'
down_revision = 'f83294852080'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Entfernen der explanations-Spalte aus der accounts-Tabelle
    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.drop_column('explanations')

    # Erstellen der account_explanations-Tabelle
    op.create_table('account_explanations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('account_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('text', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - bitte anpassen! ###
    # Löschen der account_explanations-Tabelle
    op.drop_table('account_explanations')

    # Wiederherstellen der explanations-Spalte in der accounts-Tabelle
    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('explanations', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
