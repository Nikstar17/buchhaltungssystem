# models/contact.py

import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class Contact(db.Model):
    """
    Repräsentiert einen Geschäftskontakt im Buchhaltungssystem.
    Diese Klasse speichert Informationen zu Kunden, Geschäftspartnern oder
    anderen Kontakten, die nicht als Lieferant klassifiziert sind. Kontakte
    können mit Ausgangsrechnungen und anderen Dokumenten verknüpft werden
    und enthalten alle relevanten Adress- und Kommunikationsdaten.
    """

    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=False)

    name = Column(String, nullable=False)  # Name der Kontaktperson
    phone = Column(String, nullable=False)  # Telefonnummer
    description = Column(Text, nullable=True)  # Funktion/Abteilung
