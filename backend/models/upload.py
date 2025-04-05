# models/upload.py

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from . import db


class Upload(db.Model):
    __tablename__ = "uploads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)

    filename = Column(String, nullable=False)  # Dateiname
    mimetype = Column(String, nullable=False)  # MIME-Typ (z. B. application/pdf)
    uploaded_at = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )  # Uploadzeitpunkt
    file_size = Column(Integer, nullable=False)  # Dateigröße in Bytes

    # Dateiinhalt als Base64-String
    file_content = Column(Text, nullable=False)  # Base64-kodierter Dateiinhalt
