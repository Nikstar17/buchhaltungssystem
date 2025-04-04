# models/document.py

import uuid
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, CHAR
from . import db
from .enum import document_type_enum, document_status_enum


class Document(db.Model):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    document_type = Column(document_type_enum, nullable=False)  # z. B. INCOME, EXPENSE
    status = Column(document_status_enum, nullable=False)        # z. B. OPEN, PAID

    number = Column(String, nullable=False)                      # Belegnummer
    document_date = Column(Date, nullable=False)                 # Ausstellungsdatum

    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=True)
    delivery_date = Column(Date, nullable=True)
    link_id = Column(UUID(as_uuid=True), ForeignKey("links.id"), nullable=True)
    due_date = Column(Date, nullable=True)
    cost_center_id = Column(UUID(as_uuid=True), ForeignKey("cost_centers.id"), nullable=True)

    currency_code = Column(CHAR(3), ForeignKey("currencies.code"), nullable=False)  # ISO-Code
