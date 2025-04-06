# models/cost_center.py

import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class CostCenter(db.Model):
    """
    Repräsentiert eine Kostenstelle im Buchhaltungssystem.
    Diese Klasse ermöglicht die Zuordnung von Buchungen zu bestimmten
    Unternehmensbereichen oder Projekten. Kostenstellen dienen der internen
    Kostenrechnung und erlauben eine detaillierte Analyse von Einnahmen und
    Ausgaben nach organisatorischen Einheiten, unabhängig von der
    gesetzlichen Buchführung.
    """

    __tablename__ = "cost_centers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )  # Erstellt von

    code = Column(String, nullable=False)  # Kostenstellen-Code
    name = Column(String, nullable=False)  # Bezeichnung der Kostenstelle

    active = Column(
        Boolean, nullable=False, default=True
    )  # Ist die Kostenstelle aktiv?
