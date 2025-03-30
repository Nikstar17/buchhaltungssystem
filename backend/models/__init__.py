from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .document import Document
from .booking import Booking
from .category import Category
from .account import Account