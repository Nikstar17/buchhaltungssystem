# models/supplier.py

import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class Supplier(db.Model):
    """
    Repräsentiert einen Lieferanten im Buchhaltungssystem.
    Diese Klasse speichert Informationen zu Lieferanten, mit denen das Unternehmen
    Geschäftsbeziehungen hat. Zu den gespeicherten Daten gehören Kontaktinformationen
    wie Name, Adresse, Steuernummer und Bankverbindung. Lieferanten können mit
    Eingangsrechnungen und anderen Belegen verknüpft werden.
    """

    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)  # Firmenname
    address = Column(Text, nullable=False)  # Anschrift

    tax_number = Column(String, nullable=True)  # Steuernummer
    vat_id = Column(String, nullable=True)  # USt-ID

    iban = Column(String, nullable=True)  # IBAN
    bic = Column(String, nullable=True)  # BIC

    email = Column(String, nullable=True)  # E-Mail-Adresse
    phone = Column(String, nullable=True)  # Telefonnummer
