from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
from . import db

class Document(db.Model):
    __tablename__ = 'document'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    filename = Column(String(255), nullable=False)
    upload_path = Column(String(500), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    beleg_datum = Column(Date)
    betrag = Column(Numeric(10, 2))
    kategorie_id = Column(UUID(as_uuid=True), ForeignKey('category.id'))
    beschreibung = Column(Text)
    steuerart = Column(String(20))  # Optional ENUM

    user = relationship("User", back_populates="documents")
    category = relationship("Category")