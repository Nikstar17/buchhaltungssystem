# models/auto_booking_rule.py

import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from . import db


class AutoBookingRule(db.Model):
    """
    Repräsentiert eine automatische Buchungsregel im System.
    Diese Klasse definiert Regeln für die automatische Verbuchung von Dokumenten
    basierend auf bestimmten Erkennungsmerkmalen wie Lieferant, Textmustern oder
    Beträgen. Wenn ein neues Dokument diese Kriterien erfüllt, kann das System
    die Buchung automatisch vorschlagen oder durchführen.
    """

    __tablename__ = "auto_booking_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )  # Erstellt von

    name = Column(String, nullable=False)  # Name der Regel
    description = Column(Text, nullable=True)  # Beschreibung

    supplier_id = Column(
        UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=True
    )  # Lieferant (optional)
    text_pattern = Column(String, nullable=True)  # Textmuster für die Erkennung

    account_id = Column(
        UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False
    )  # Zielkonto für die Buchung
    tax_rate_id = Column(
        UUID(as_uuid=True), ForeignKey("tax_rates.id"), nullable=True
    )  # Steuersatz (optional)

    active = Column(Boolean, nullable=False, default=True)  # Ist die Regel aktiv?
