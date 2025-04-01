from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from . import db
import uuid

class Upload(db.Model):
    __tablename__ = "uploads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Upload-ID
    document_id = Column(UUID(as_uuid=True), ForeignKey("document.id"), nullable=False)  # Zugehöriger Beleg
    filename = Column(String, nullable=False)  # Dateiname
    file_path = Column(String, nullable=False)  # Pfad zur Datei
    mimetype = Column(String, nullable=False)  # MIME-Type (z. B. application/pdf)
    uploaded_at = Column(DateTime, nullable=False, server_default=text("NOW()"))
    file_size = Column(Integer, nullable=False)  # Dateigröße in Bytes
