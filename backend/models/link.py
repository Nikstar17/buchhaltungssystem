from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

class Link(db.Model):
    __tablename__ = "link"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
