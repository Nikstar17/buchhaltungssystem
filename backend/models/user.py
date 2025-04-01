from sqlalchemy import Column, String, DateTime, Enum, text
from sqlalchemy.dialects.postgresql import UUID
from flask_bcrypt import Bcrypt
import uuid
from . import db

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, server_default=text("NOW()"))

    email = Column(String, nullable=False, unique=True)    # E-Mail ist eindeutig
    password_hash = Column(String, nullable=False)
    role = Column(Enum("USER", "ADMIN", name="role"), nullable=False, server_default="USER")

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    street = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)

    # Passwort-Property (schreibgeschützt)
    @property
    def password(self):
        raise AttributeError("Passwort kann nicht gelesen werden.")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
