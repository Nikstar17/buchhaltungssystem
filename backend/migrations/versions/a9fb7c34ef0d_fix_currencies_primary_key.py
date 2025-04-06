"""fix currencies primary key

Revision ID: a9fb7c34ef0d
Revises: ce3f67629bcf
Create Date: 2025-04-05 18:43:07.557963

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a9fb7c34ef0d"
down_revision = "ce3f67629bcf"
branch_labels = None
depends_on = None


def upgrade():
    # Entfernen der Fremdschlüsselbeziehung, die den Primary Key verwendet
    op.drop_constraint("documents_currency_code_fkey", "documents", type_="foreignkey")

    # Hinzufügen der id-Spalte und Ändern des Primary Keys für die currencies-Tabelle
    with op.batch_alter_table("currencies", schema=None) as batch_op:
        # UUID-Spalte hinzufügen
        batch_op.add_column(sa.Column("id", sa.UUID(), nullable=False))
        # Unique-Constraint für code beibehalten
        batch_op.create_unique_constraint("currencies_code_key", ["code"])
        # Bestehenden Primary Key (code) entfernen
        batch_op.drop_constraint("currencies_pkey", type_="primary")
        # Neuen Primary Key auf id setzen
        batch_op.create_primary_key("currencies_pkey", ["id"])

    # In der nächsten Migration wird die Fremdschlüsselbeziehung von
    # documents.currency_id zu currencies.id erstellt


def downgrade():
    # Ändern des Primary Keys zurück auf code
    with op.batch_alter_table("currencies", schema=None) as batch_op:
        # Primary Key auf id entfernen
        batch_op.drop_constraint("currencies_pkey", type_="primary")
        # Primary Key auf code setzen
        batch_op.create_primary_key("currencies_pkey", ["code"])
        # Unique-Constraint für code entfernen (wird durch PK ersetzt)
        batch_op.drop_constraint("currencies_code_key", type_="unique")
        # id-Spalte entfernen
        batch_op.drop_column("id")

    # Wiederherstellen der Fremdschlüsselbeziehung
    op.create_foreign_key(
        "documents_currency_code_fkey",
        "documents",
        "currencies",
        ["currency_code"],
        ["code"],
    )
