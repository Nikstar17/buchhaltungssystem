# models/document_number_range.py

import uuid
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db
from .enum import document_type_enum


class DocumentNumberRange(db.Model):
    """
    Repräsentiert einen Belegnummernkreis im Buchhaltungssystem.
    Diese Klasse verwaltet die automatische Vergabe von Belegnummern für verschiedene
    Dokumenttypen wie Rechnungen, Gutschriften oder Quittungen. Für jeden Typ kann
    ein separater Nummernkreis mit spezifischem Präfix und Zähler definiert werden,
    was eine geordnete und konforme Belegnummerierung sicherstellt.
    """

    __tablename__ = "document_number_ranges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )  # Erstellt von

    year = Column(Integer, nullable=False)  # Jahr des Nummernkreises
    type = Column(document_type_enum, nullable=False)  # Dokumenttyp (INCOME/EXPENSE)
    current_number = Column(Integer, nullable=False)  # Aktueller Zählerstand
