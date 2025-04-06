# models/category.py

import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class Category(db.Model):
    """
    Repräsentiert eine Kategorie für die Klassifizierung von Buchungspositionen.
    Diese Klasse ermöglicht die zusätzliche Klassifizierung von Rechnungspositionen
    und anderen buchhalterischen Entitäten unabhängig vom Kontenrahmen. Kategorien
    können in Berichten und Auswertungen verwendet werden, um Ausgaben oder Einnahmen
    nach benutzerdefinierten Kriterien zu gruppieren.
    """

    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )  # Erstellt von

    name = Column(String, nullable=False)  # Name der Kategorie
    color = Column(
        String, nullable=True
    )  # Optionale Farbcodierung (z.B. für visuelle Darstellung)
