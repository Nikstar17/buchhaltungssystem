from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String, Date, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from . import db

class Booking(db.Model):
    __tablename__ = 'booking'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    datum = Column(Date, nullable=False)
    art = Column(String(10), nullable=False)  # Einnahme / Ausgabe
    betrag = Column(Numeric(10, 2), nullable=False)
    konto_id = Column(UUID(as_uuid=True), ForeignKey('account.id'))
    gegenkonto = Column(String(100))
    kategorie_id = Column(UUID(as_uuid=True), ForeignKey('category.id'))
    beleg_id = Column(UUID(as_uuid=True), ForeignKey('document.id'))
    beschreibung = Column(Text)

    user = relationship("User", back_populates="bookings")
    account = relationship("Account")
    category = relationship("Category")
    document = relationship("Document")
    links = relationship("Link", back_populates="booking")