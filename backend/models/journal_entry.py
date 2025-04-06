# models/journal_entry.py

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class JournalEntry(db.Model):
    """
    Repräsentiert einen vollständigen Buchungssatz in der Buchhaltung.
    Ein Buchungssatz ist die grundlegende Einheit der doppelten Buchführung und besteht
    aus mindestens zwei Buchungszeilen (JournalLine), wobei die Summe der Soll- und Haben-Seiten
    ausgeglichen sein muss. Der Buchungssatz kann mit Belegen, Dokumenten und anderen
    buchhalterischen Entitäten verknüpft sein.
    """

    __tablename__ = "journal_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True
    )  # Optionaler Belegbezug

    date = Column(Date, nullable=False)  # Buchungsdatum
    description = Column(String, nullable=True)  # Buchungstext
    created_at = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )  # Erstellungszeit
