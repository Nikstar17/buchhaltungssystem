# models/fiscal_period.py

import uuid
from sqlalchemy import Column, String, Date, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class FiscalPeriod(db.Model):
    """
    Repräsentiert eine Buchungsperiode im Geschäftsjahr.
    Diese Klasse definiert buchhalterische Zeiträume wie Monate oder Quartale
    eines Geschäftsjahres. Jede Buchungsperiode hat einen festgelegten Anfangs- und
    Endzeitpunkt und kann entweder offen oder geschlossen sein. Buchungen können
    nur in offene Perioden vorgenommen werden.
    """

    __tablename__ = "fiscal_periods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )  # Erstellt von

    name = Column(String, nullable=False)  # Name der Periode (z.B. "Januar 2025")
    start_date = Column(Date, nullable=False)  # Beginn der Periode
    end_date = Column(Date, nullable=False)  # Ende der Periode

    closed = Column(
        Boolean, nullable=False, default=False
    )  # Ist die Periode abgeschlossen?
