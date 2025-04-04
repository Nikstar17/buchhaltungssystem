# models/payment.py

import uuid
from sqlalchemy import Column, String, Numeric, Date, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)       # Zugehöriger Beleg
    payment_date = Column(Date, nullable=False)                                                # Zahlungsdatum
    amount = Column(Numeric, nullable=False)                                                   # Betrag
    method = Column(String, nullable=False)                                                    # Zahlungsart
    comment = Column(Text, nullable=True)                                                      # Kommentar
    bank_account_id = Column(UUID(as_uuid=True), ForeignKey("bank_accounts.id"), nullable=False)  # Bankkonto
