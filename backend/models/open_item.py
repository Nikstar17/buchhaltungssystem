# models/open_item.py

import uuid
from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db


class OpenItem(db.Model):
    __tablename__ = "open_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)

    open_amount = Column(Numeric, nullable=False)  # Offener Betrag
    due_date = Column(Date, nullable=True)         # Fälligkeitsdatum
    status = Column(String, nullable=False)        # z. B. "offen", "teilbezahlt", "bezahlt"
