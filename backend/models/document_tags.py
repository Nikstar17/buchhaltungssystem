from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db

class DocumentTag(db.Model):
    __tablename__ = "document_tags"

    document_id = Column(UUID(as_uuid=True), ForeignKey("document.id"), primary_key=True, nullable=False)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True, nullable=False)
