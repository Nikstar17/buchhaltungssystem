from sqlalchemy import Column, Numeric, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

class LineItem(db.Model):
    __tablename__ = "line_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("document.id"), nullable=False)

    line_number = Column(Integer, nullable=False)           # z. B. Position 1, 2, 3
    description = Column(String, nullable=False)            # Artikel- oder Leistungsbeschreibung
    quantity = Column(Numeric, nullable=False)              # Menge
    unit_price = Column(Numeric, nullable=False)            # Einzelpreis
    total_price = Column(Numeric, nullable=False)           # Gesamtpreis (Menge × Preis)

    category_id = Column(UUID(as_uuid=True), ForeignKey("category.id"), nullable=True)
    tax_rate_id = Column(UUID(as_uuid=True), ForeignKey("tax_rate.id"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=True)
