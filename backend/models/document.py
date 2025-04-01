from sqlalchemy import Column, Date, String, Enum, ForeignKey, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

class Document(db.Model):
    __tablename__ = "document"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    document_type = Column(
        Enum("INCOME", "EXPENSE", name="document_type"),
        nullable=False
    )  # Eingangs- oder Ausgangsbeleg

    status = Column(
        Enum("OPEN", "PAID", "CANCELLED", "OVERDUE", name="document_status"),
        nullable=False
    )  # Status des Belegs

    number = Column(String, nullable=False)  # Belegnummer (intern oder extern)
    document_date = Column(Date, nullable=False)  # Ausstellungsdatum

    supplier_id = Column(UUID(as_uuid=True), ForeignKey("supplier.id"), nullable=True)
    delivery_date = Column(Date, nullable=True)
    link_id = Column(UUID(as_uuid=True), ForeignKey("link.id"), nullable=True)
    due_date = Column(Date, nullable=True)
    cost_center_id = Column(UUID(as_uuid=True), ForeignKey("cost_center.id"), nullable=True)
    currency_code = Column(CHAR(3), ForeignKey("currency.code"), nullable=False)
