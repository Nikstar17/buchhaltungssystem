# models/upload.py

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class Upload(db.Model):
    """
    Repräsentiert eine hochgeladene Datei im Buchhaltungssystem.
    Diese Klasse speichert Informationen zu hochgeladenen Dokumenten wie Rechnungen,
    Quittungen oder anderen buchhalterischen Belegen. Zu den gespeicherten Daten
    gehören Dateiname, MIME-Typ, Zeitstempel und optionale Verknüpfungen zu
    anderen Entitäten wie Dokumenten.
    """

    __tablename__ = "uploads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    filename = Column(String, nullable=False)  # Originaler Dateiname
    mimetype = Column(String, nullable=False)  # MIME-Typ der Datei

    file_data = Column(Text, nullable=True)

    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True
    )  # Optionale Verknüpfung zu einem Dokument
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Hochgeladen von

    uploaded_at = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )  # Hochladezeitpunkt
    processed = Column(
        Boolean, nullable=False, default=False
    )  # Wurde die Datei bereits verarbeitet?
