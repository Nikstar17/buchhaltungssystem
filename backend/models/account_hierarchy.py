import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from . import db


class AccountHierarchy(db.Model):
    """
    Repräsentiert die hierarchische Struktur eines Kontos im Kontenrahmen.
    Diese Klasse speichert Informationen über die Kontenklasse, Kontengruppe und Kontenart
    eines Kontos gemäß dem Standardkontenrahmen (z.B. SKR04).
    """

    __tablename__ = "account_hierarchies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    account = relationship("Account", back_populates="hierarchy")

    # Kontenklasse (z.B. "6" für "Betriebliche Aufwendungen")
    class_number = Column(String, nullable=True)
    class_name = Column(String, nullable=True)

    # Kontengruppe (z.B. "69" für "Sonstige betriebliche Aufwendungen")
    group_number = Column(String, nullable=True)
    group_name = Column(String, nullable=True)

    # Kontenart (z.B. "692" für "Sonstige betriebliche Aufwendungen")
    type_number = Column(String, nullable=True)
    type_name = Column(String, nullable=True)

    # Verwandte Konten als JSON-Feld
    related_accounts = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<AccountHierarchy {self.class_number}/{self.group_number}/{self.type_number}>"