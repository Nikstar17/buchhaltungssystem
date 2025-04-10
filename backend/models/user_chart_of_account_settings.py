import uuid
from sqlalchemy import Column, ForeignKey, Boolean, String, Text
from sqlalchemy.dialects.postgresql import UUID
from . import db

class UserChartOfAccountSettings(db.Model):
    """
    Speichert die benutzerspezifischen Einstellungen für Konten.
    Diese Tabelle verknüpft Benutzer mit individuellen Konten-Einstellungen
    wie Aktivierung/Deaktivierung.
    """

    __tablename__ = "user_chart_of_account_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)

    # Einstellungen
    is_active = Column(Boolean, nullable=False, default=True)

    custom_name = Column(String, nullable=True)  # Benutzerdefinierter Name
    custom_description = Column(Text, nullable=True)  # Benutzerdefinierte Beschreibung
    favorite = Column(Boolean, nullable=False, default=False)  # Als Favorit markiert

    __table_args__ = (
        db.UniqueConstraint('user_id', 'account_id', name='uix_user_chart_account'),
)