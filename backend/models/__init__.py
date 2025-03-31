from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .document import Document
from .booking import Booking
from .category import Category
from .account import Account
from .costcenter import CostCenter
from .link import Link  # Sicherstellen, dass Link importiert ist
from .tag import Tag  # Sicherstellen, dass Tag importiert ist
from .document_tag import document_tag  # Sicherstellen, dass document_tag importiert ist