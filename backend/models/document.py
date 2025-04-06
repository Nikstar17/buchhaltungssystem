# models/document.py

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Date,
    DateTime,
    Numeric,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from . import db
from .enum import document_type_enum, document_status_enum


class Document(db.Model):
    """
    Repräsentiert einen Buchhaltungsbeleg wie Rechnung, Gutschrift oder Quittung.
    Diese Klasse speichert alle relevanten Informationen zu einem Beleg, einschließlich
    Beleg-Typ (Eingang/Ausgang), Status, Beträge, Datumsangaben und Verknüpfungen zu
    anderen Entitäten wie Lieferanten oder Kundennummern. Zu jedem Dokument können
    Einzelpositionen (LineItems) sowie Buchungssätze (JournalEntries) erstellt werden.
    """

    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Benutzer
    document_number = Column(String, nullable=False)  # Belegnummer
    document_type = Column(document_type_enum, nullable=False)  # INCOME / EXPENSE (Ausgang / Eingang)
    status = Column(document_status_enum, nullable=False, default="OPEN")  # Status des Belegs
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=True)  # Lieferant
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=True)  # Kontakt
    issue_date = Column(Date, nullable=False)  # Ausstellungsdatum / Belegdatum
    due_date = Column(Date, nullable=True)  # Fälligkeitsdatum
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=False)  # Währung
    is_posted = Column(Boolean, nullable=False, default=False)  # Flag für Buchungsstatus
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))  # Erstelldatum
