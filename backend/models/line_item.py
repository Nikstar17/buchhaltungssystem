# models/line_item.py

import uuid
from sqlalchemy import Column, String, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class LineItem(db.Model):
    __tablename__ = "line_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)

    line_number = Column(Integer, nullable=False)         # Positionsnummer
    description = Column(String, nullable=False)          # Beschreibung
    quantity = Column(Numeric, nullable=False)            # Menge
    unit_price = Column(Numeric, nullable=False)          # Einzelpreis
    total_price = Column(Numeric, nullable=False)         # Gesamtpreis

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    tax_rate_id = Column(UUID(as_uuid=True), ForeignKey("tax_rates.id"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True)
