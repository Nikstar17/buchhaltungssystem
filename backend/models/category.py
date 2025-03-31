from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db

class Category(db.Model):
    __tablename__ = 'category'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(String(20))  # Einnahme, Ausgabe, gemischt

    user = relationship("User", back_populates="categories")
    links = relationship("Link", back_populates="category")