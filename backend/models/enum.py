from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from . import db


# === ENUM Typen für PostgreSQL ===

account_type_enum = PgEnum(
    "ASSET",  # Aktivkonto (z. B. Bank, Forderungen)
    "LIABILITY",  # Passivkonto (z. B. Verbindlichkeiten)
    "EQUITY",  # Eigenkapitalkonto
    "REVENUE",  # Erlöskonto
    "EXPENSE",  # Aufwandskonto
    name="account_type",
    create_type=True,
)

document_type_enum = PgEnum(
    "INCOME",  # Ausgangsbeleg (z. B. Rechnung)
    "EXPENSE",  # Eingangsbeleg (z. B. Eingangsrechnung)
    name="document_type",
    create_type=True,
)

document_status_enum = PgEnum(
    "OPEN",  # Offen
    "PAID",  # Bezahlt
    "CANCELLED",  # Storniert
    "OVERDUE",  # Überfällig
    name="document_status",
    create_type=True,
)

role_enum = PgEnum(
    "USER",  # Normaler Benutzer
    "ADMIN",  # Administrator mit erweiterten Rechten
    name="role",
    create_type=True,
)

side_enum = PgEnum("DEBIT", "CREDIT", name="side", create_type=True)  # Soll  # Haben
