from sqlalchemy import Column, Boolean, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

class Account(db.Model):
    __tablename__ = "account"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chart_of_accounts_id = Column(UUID(as_uuid=True), ForeignKey("chart_of_accounts.id"), nullable=False)
    number = Column(String, nullable=False)  # z. B. '4400'
    name = Column(String, nullable=False)    # z. B. 'Mietaufwand'
    type = Column(String, nullable=False)    # z. B. 'AUFWAND', 'ERLÖS'
    active = Column(Boolean, nullable=False, server_default=text('true'))
