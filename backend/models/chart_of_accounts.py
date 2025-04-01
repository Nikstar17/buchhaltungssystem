from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

class ChartOfAccounts(db.Model):
    __tablename__ = "chart_of_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    name = Column(String, nullable=False)           # z. B. "SKR04"
    description = Column(Text, nullable=True)       # Optional: Beschreibung
