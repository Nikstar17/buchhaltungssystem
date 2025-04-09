# models/user.py

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from flask_bcrypt import Bcrypt
from . import db
from .enum import role_enum

bcrypt = Bcrypt()


class User(db.Model):
    """
    Repräsentiert einen Benutzer des Buchhaltungssystems.
    Diese Klasse speichert Benutzerinformationen wie Name, E-Mail und Passwort
    sowie Berechtigungen und Einstellungen. Benutzer können verschiedene Rollen
    haben (z.B. normaler Benutzer oder Administrator) und werden zur Nachverfolgung
    von Änderungen und für die Zugriffssteuerung verwendet.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    email = Column(String, nullable=False, unique=True)  # E-Mail-Adresse
    password_hash = Column(String, nullable=False)  # Gehashter Login

    role = Column(role_enum, nullable=False, default="USER")  # Benutzerrolle

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    street = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)

    chart_of_accounts_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chart_of_accounts.id"),
        nullable=True
    )  # Referenz auf den vom Benutzer verwendeten Kontenrahmen

    @property
    def password(self):
        raise AttributeError("Passwort kann nicht gelesen werden.")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
