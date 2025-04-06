# models/chart_of_accounts.py

import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from . import db


class ChartOfAccounts(db.Model):
    """
    Repräsentiert einen Kontenrahmen im Buchhaltungssystem.
    Ein Kontenrahmen ist eine strukturierte Sammlung von Konten, die als Vorlage für die
    Buchführung dient. In Deutschland werden häufig Standard-Kontenrahmen wie SKR03 oder SKR04
    verwendet. Diese Klasse enthält grundlegende Informationen zum Kontenrahmen und definiert,
    welche Konten für die Buchführung zur Verfügung stehen.
    """

    __tablename__ = "chart_of_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )  # Erstellt von (kann NULL sein bei Standardkontenrahmen)
    is_standard = Column(
        Boolean, nullable=False, default=False
    )  # Ist ein Standard-Kontenrahmen
    is_active = Column(Boolean, nullable=False, default=True)  # Ist aktiv

    name = Column(String, nullable=False)  # Name des Kontenrahmens (z.B. "SKR04")
    description = Column(Text, nullable=True)  # Beschreibung
