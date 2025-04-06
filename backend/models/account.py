import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from . import db
from .enum import account_type_enum


class Account(db.Model):
    """
    Repräsentiert ein Konto im Buchhaltungsplan (Kontenrahmen).
    Diese Klasse bildet die Grundlage für die doppelte Buchführung und definiert
    die verschiedenen Konten wie Aktivkonten, Passivkonten, Ertrags- und Aufwandskonten.
    Jedes Konto hat eine eindeutige Nummer und ist einem bestimmten Kontotyp zugeordnet.
    Konten können hierarchisch strukturiert sein und einem Kontenrahmen zugeordnet werden.
    """

    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chart_of_accounts_id = Column(
        UUID(as_uuid=True), ForeignKey("chart_of_accounts.id"), nullable=False
    )  # Zugehöriger Kontenrahmen

    parent_id = Column(
        UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True
    )  # Übergeordnetes Konto (für Hierarchie)
    children = relationship("Account", backref=backref("parent", remote_side=[id]))

    tax_rate_id = Column(
        UUID(as_uuid=True), ForeignKey("tax_rates.id"), nullable=True
    )  # Zugehöriger Steuersatz
    tax_rate = relationship("TaxRate", foreign_keys=[tax_rate_id])

    number = Column(String, nullable=False)  # Kontonummer
    name = Column(String, nullable=False)  # Kontoname
    type = Column(
        account_type_enum, nullable=False
    )  # Kontotyp: ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE
    level = Column(Integer, nullable=True)  # Hierarchietiefe
    active = Column(
        Boolean, nullable=False, default=True
    )  # Zeigt an, ob das Konto aktiv ist
