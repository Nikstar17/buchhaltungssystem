from sqlalchemy import Column, Boolean, Date, Numeric, String, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

class TaxRate(db.Model):
    __tablename__ = "tax_rate"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)              # z. B. "USt 19%"
    percentage = Column(Numeric, nullable=False)       # z. B. 19.00
    valid_from = Column(Date, nullable=False)          # Ab wann gültig
    active = Column(Boolean, nullable=False, server_default=text('true'))  # Aktiv-Status
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)  # Optional: Benutzer, der den Satz erstellt hat