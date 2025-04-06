# models/document_tag.py

import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class DocumentTag(db.Model):
    """
    Repräsentiert die Verknüpfung zwischen einem Dokument und einem Tag.
    Diese Klasse dient als Verbindungstabelle für die Viele-zu-Viele-Beziehung
    zwischen Dokumenten und Tags. Sie ermöglicht die Zuordnung mehrerer Tags zu
    einem Dokument und unterstützt damit die flexible Kategorisierung und
    Filterung von Buchhaltungsbelegen.
    """

    __tablename__ = "document_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False
    )  # Dokument-Referenz
    tag_id = Column(
        UUID(as_uuid=True), ForeignKey("tags.id"), nullable=False
    )  # Tag-Referenz
