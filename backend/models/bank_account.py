# models/bank_account.py

import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class BankAccount(db.Model):
    """
    Repräsentiert ein Bankkonto im Buchhaltungssystem.
    Diese Klasse speichert Informationen zu Bankkonten des Unternehmens,
    einschließlich Name, IBAN, BIC und Bankname. Jedes Bankkonto ist einem
    bestimmten Buchungskonto zugeordnet und kann für Zahlungen verwendet werden.
    """

    __tablename__ = "bank_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)  # Anzeigename des Kontos
    iban = Column(String, nullable=False)  # IBAN
    bic = Column(String, nullable=False)  # BIC
    bank_name = Column(String, nullable=False)  # Name der Bank
    active = Column(Boolean, nullable=False, default=True)  # Konto aktiv?
