import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from . import db


class AccountExplanation(db.Model):
    """
    Repräsentiert eine Erläuterung zu einem Konto im Kontenrahmen.
    Diese Klasse speichert detaillierte Erläuterungen mit verschiedenen Typen wie 'SB', 'F', 'KU', etc.
    """

    __tablename__ = "account_explanations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    account = relationship("Account", back_populates="explanations")

    # Typ der Erläuterung (z.B. 'SB', 'F', 'KU', '#xxxx', etc.)
    type = Column(String, nullable=True)

    # Text der Erläuterung
    text = Column(Text, nullable=True)

    def __repr__(self):
        return f"<AccountExplanation {self.type}: {self.text[:30]}...>"