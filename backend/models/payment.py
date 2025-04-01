from sqlalchemy import Column, Date, String, ForeignKey, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

class Payment(db.Model):
    __tablename__ = "payment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("document.id"), nullable=False)
    payment_date = Column(Date, nullable=False)                   # Datum der Zahlung
    amount = Column(Numeric, nullable=False)                      # Betrag der Zahlung
    method = Column(String, nullable=False)                       # Zahlungsmethode (z. B. Überweisung)
    comment = Column(Text, nullable=True)                         # Optionaler Kommentar oder Vermerk
    bank_account_id = Column(UUID(as_uuid=True), ForeignKey("bank_account.id"), nullable=False)
