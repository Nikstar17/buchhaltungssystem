# models/chart_of_accounts.py

import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from . import db


class ChartOfAccounts(db.Model):
    __tablename__ = "chart_of_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_standard = Column(Boolean, nullable=False, default=False) # Kennzeichnung für Standard-Kontenrahmen

    name = Column(String, nullable=False)        # z. B. "SKR04"
    description = Column(Text, nullable=True)    # Optional: Beschreibung
