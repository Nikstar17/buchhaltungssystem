from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from . import db

class Tag(db.Model):
    __tablename__ = 'tag'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)  # Name des Tags

    # Beziehung zu Belegen
    documents = relationship(
        "Document",
        secondary="document_tag",
        back_populates="tags"
    )