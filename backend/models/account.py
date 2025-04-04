import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from . import db
from .enum import account_type_enum


class Account(db.Model):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chart_of_accounts_id = Column(UUID(as_uuid=True), ForeignKey("chart_of_accounts.id"), nullable=False)

    parent_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True)  # ← Hierarchie!
    children = relationship("Account", backref=backref("parent", remote_side=[id]))

    number = Column(String, nullable=False)  # z. B. '4400'
    name = Column(String, nullable=False)    # z. B. 'Mietaufwand'
    type = Column(account_type_enum, nullable=False)  # ENUM: ASSET, EXPENSE, etc.
    level = Column(Integer, nullable=True)  # z. B. 1=Hauptgruppe, 2=Gruppe, 3=Einzelkonto
    active = Column(Boolean, nullable=False, default=True)
