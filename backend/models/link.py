# models/link.py

import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class Link(db.Model):
    """
    Repräsentiert eine Verknüpfung zwischen zwei Dokumenten im Buchhaltungssystem.
    Diese Klasse ermöglicht das Erstellen von Beziehungen zwischen verschiedenen
    Buchhaltungsbelegen, z.B. zwischen einer Rechnung und einer zugehörigen Gutschrift
    oder zwischen mehreren zusammengehörigen Belegen. Die Verknüpfungen helfen dabei,
    den Überblick über zusammenhängende Transaktionen zu behalten.
    """

    __tablename__ = "links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    source_document_id = Column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False
    )  # Quelldokument
    target_document_id = Column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False
    )  # Zieldokument

    link_type = Column(
        String, nullable=False
    )  # Art der Verknüpfung (z.B. "gutschrift_zu_rechnung", "folgebeleg")
