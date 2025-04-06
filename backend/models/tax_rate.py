# models/tax_rate.py

import uuid
from sqlalchemy import Column, String, Numeric, Date, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class TaxRate(db.Model):
    """
    Repräsentiert einen Steuersatz für die Buchhaltung.
    Diese Klasse definiert verschiedene Steuersätze (wie z.B. Mehrwertsteuer)
    mit ihren Prozentsätzen, die auf Konten, Rechnungspositionen oder
    Buchungszeilen angewendet werden können. Ein Steuersatz kann aktiv oder
    inaktiv sein und wird für die korrekte Berechnung und Ausweisung von
    Steuerbeträgen verwendet.
    """

    __tablename__ = "tax_rates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)  # Bezeichnung (z. B. "MwSt 19%")
    percentage = Column(Numeric, nullable=False)  # Steuersatz in Prozent
    valid_from = Column(Date, nullable=False)  # Gültig ab
    active = Column(Boolean, nullable=False, default=True)  # Aktiv?

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )  # Erstellt von
