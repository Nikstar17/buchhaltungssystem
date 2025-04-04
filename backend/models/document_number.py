# models/document_number_range.py

import uuid
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db
from .enum import document_type_enum


class DocumentNumberRange(db.Model):
    __tablename__ = "document_number_ranges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    year = Column(Integer, nullable=False)                         # Jahr (z. B. 2025)
    type = Column(document_type_enum, nullable=False)              # Belegtyp (INCOME / EXPENSE)
    current_number = Column(Integer, nullable=False)               # Aktueller Zählerstand
