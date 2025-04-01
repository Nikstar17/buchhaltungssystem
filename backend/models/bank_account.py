from sqlalchemy import Column, Boolean, String, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

class BankAccount(db.Model):
    __tablename__ = "bank_account"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    name = Column(String, nullable=False)           # z. B. "Sparkasse Geschäftskonto"
    iban = Column(String, nullable=False)
    bic = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, server_default=text('true'))
