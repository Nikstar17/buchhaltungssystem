from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

class Supplier(db.Model):
    __tablename__ = "supplier"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)         # Firmenname
    address = Column(Text, nullable=False)        # Anschrift
    tax_number = Column(String, nullable=True)    # Steuernummer (national)
    vat_id = Column(String, nullable=True)        # USt-IdNr. (EU-Ausland)
    iban = Column(String, nullable=True)          # Bankverbindung
    bic = Column(String, nullable=True)
    email = Column(String, nullable=True)         # Kontaktadresse
    phone = Column(String, nullable=True)         # Telefonnummer
