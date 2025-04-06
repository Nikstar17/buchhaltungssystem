# models/tag.py

import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class Tag(db.Model):
    """
    Repräsentiert ein Schlagwort (Tag) im Buchhaltungssystem.
    Diese Klasse ermöglicht die flexible Kennzeichnung von Dokumenten und anderen
    Entitäten mit benutzerdefinierten Schlagwörtern. Tags erleichtern das Auffinden
    und Organisieren von buchhalterischen Informationen und können für individuelles
    Reporting genutzt werden.
    """

    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )  # Erstellt von

    name = Column(String, nullable=False)  # Name des Tags
    color = Column(
        String, nullable=True
    )  # Optionale Farbcodierung für visuelle Darstellung
