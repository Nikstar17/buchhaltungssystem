from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String, Date, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from . import db

class CostCenter(db.Model):
    __tablename__ = 'costcenter'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    user = relationship("User", back_populates="costcenters")
    links = relationship("Link", back_populates="costcenter")

