# models/currency.py

import uuid
from sqlalchemy import Column, String, Boolean, Numeric, CHAR
from sqlalchemy.dialects.postgresql import UUID
from . import db


class Currency(db.Model):
    """
    Repräsentiert eine Währung im Buchhaltungssystem.
    Diese Klasse definiert die im System verfügbaren Währungen mit ihren
    Codes und Symbolen. Jede Währung kann als Standardwährung festgelegt werden
    und wird für die Wertangabe bei Dokumenten, Buchungen und anderen
    finanzrelevanten Entitäten verwendet.
    """

    __tablename__ = "currencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    code = Column(CHAR(3), nullable=False, unique=True)  # Währungscode (z.B. EUR, USD)
    name = Column(String, nullable=False)  # Name (z.B. Euro, US-Dollar)
    symbol = Column(String, nullable=False)  # Symbol (z.B. €, $)
    base_rate = Column(Numeric, nullable=False)  # Umrechnung zur Basiswährung

    is_default = Column(Boolean, nullable=False, default=False)  # Ist Standardwährung
    is_active = Column(Boolean, nullable=False, default=True)  # Ist aktiv
