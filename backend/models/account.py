from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db

class Account(db.Model):
    __tablename__ = 'account'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    name = Column(String(100), nullable=False)
    nummer = Column(String(10))

    user = relationship("User", back_populates="accounts")