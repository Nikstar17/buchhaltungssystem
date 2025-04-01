from sqlalchemy import Column, String, Numeric, CHAR
from . import db

class Currency(db.Model):
    __tablename__ = "currency"

    code = Column(CHAR(3), primary_key=True)            # ISO-Code (z. B. EUR, USD)
    name = Column(String, nullable=False)               # Name der Währung (z. B. Euro)
    symbol = Column(String, nullable=False)             # Symbol (z. B. €, $)
    base_rate = Column(Numeric, nullable=False)         # Umrechnung zur Basiswährung (z. B. EUR = 1.0)
