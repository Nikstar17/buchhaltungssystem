# models/auto_booking_rule.py

import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class AutoBookingRule(db.Model):
    __tablename__ = "auto_booking_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    match_string = Column(String, nullable=False)                         # z. B. "Dropbox"
    default_account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True)
    default_tax_rate_id = Column(UUID(as_uuid=True), ForeignKey("tax_rates.id"), nullable=True)
