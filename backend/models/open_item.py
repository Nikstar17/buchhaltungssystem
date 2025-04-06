# models/open_item.py

import uuid
from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class OpenItem(db.Model):
    """
    Repräsentiert einen offenen Posten im Buchhaltungssystem.
    Diese Klasse verfolgt unbezahlte oder teilweise bezahlte Forderungen und
    Verbindlichkeiten. Offene Posten entstehen, wenn Rechnungen erstellt oder
    empfangen werden, und werden geschlossen, wenn die vollständige Zahlung
    erfolgt ist. Sie sind zentral für das Forderungs- und Verbindlichkeitenmanagement.
    """

    __tablename__ = "open_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False
    )  # Zugehöriges Dokument

    open_amount = Column(Numeric, nullable=False)  # Offener Betrag
    due_date = Column(Date, nullable=True)  # Fälligkeitsdatum
    status = Column(String, nullable=False)  # z. B. "offen", "teilbezahlt", "bezahlt"
