# models/link.py

import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from . import db


class Link(db.Model):
    __tablename__ = "links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
