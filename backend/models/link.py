from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from . import db

class Link(db.Model):
    __tablename__ = 'link'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey('document.id'), nullable=True)
    booking_id = Column(UUID(as_uuid=True), ForeignKey('booking.id'), nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey('category.id'), nullable=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey('account.id'), nullable=True)
    costcenter_id = Column(UUID(as_uuid=True), ForeignKey('costcenter.id'), nullable=True)

    # Beziehungen
    document = relationship("Document", back_populates="links")
    booking = relationship("Booking", back_populates="links")
    category = relationship("Category", back_populates="links")
    account = relationship("Account", back_populates="links")
    costcenter = relationship("CostCenter", back_populates="links")