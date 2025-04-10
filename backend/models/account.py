import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from . import db
from .enum import account_type_enum


class Account(db.Model):
    """
    Repräsentiert ein Konto im Buchhaltungsplan (Kontenrahmen).
    Diese Klasse bildet die Grundlage für die doppelte Buchführung und definiert
    die verschiedenen Konten wie Aktivkonten, Passivkonten, Ertrags- und Aufwandskonten.
    Jedes Konto hat eine eindeutige Nummer und ist einem bestimmten Kontotyp zugeordnet.
    Konten können einem Kontenrahmen zugeordnet werden.
    """

    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chart_of_accounts_id = Column(UUID(as_uuid=True), ForeignKey("chart_of_accounts.id"), nullable=False)  # Zugehöriger Kontenrahmen

    tax_rate_id = Column(UUID(as_uuid=True), ForeignKey("tax_rates.id"), nullable=True)  # Zugehöriger Steuersatz
    tax_rate = relationship("TaxRate", foreign_keys=[tax_rate_id])

    number = Column(String, nullable=False)  # Kontonummer
    name = Column(String, nullable=False)  # Kontoname
    type = Column(account_type_enum, nullable=False)  # Kontotyp: ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE
    active = Column(Boolean, nullable=False, default=True)  # Zeigt an, ob das Konto aktiv ist

    # Beziehung zu den Erläuterungen
    explanations = relationship("AccountExplanation", back_populates="account", cascade="all, delete-orphan")

    # Felder für SKR04-Import
    description = Column(Text, nullable=True)  # Beschreibung/Erläuterung des Kontos
    account_class = Column(String, nullable=True)  # Kontenklasse (z.B. "Anlagevermögenskonten")
    account_group = Column(String, nullable=True)  # Kontengruppe
    account_type_custom = Column(String, nullable=True)  # Kontenart

    # Taxonomie-Informationen
    taxonomy_element = Column(String, nullable=True)  # Hauptelement der Taxonomie
    taxonomy_type = Column(String, nullable=True)  # Typ der Taxonomie (Asset, Liability, etc.)

    # Erweiterte Informationen im JSON-Format
    related_accounts = Column(JSON, nullable=True)  # Verwandte Konten

    def __repr__(self):
        return f"<Account {self.number}: {self.name}>"
