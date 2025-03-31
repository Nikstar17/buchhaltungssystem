from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash
import uuid
import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from . import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    documents = relationship("Document", back_populates="user")
    bookings = relationship("Booking", back_populates="user")
    categories = relationship("Category", back_populates="user")
    accounts = relationship("Account", back_populates="user")

    @property
    def password(self):
        raise AttributeError("Passwort kann nicht gelesen werden.")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)