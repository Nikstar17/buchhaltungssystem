# models/journal_line.py

import uuid
from sqlalchemy import Column, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import db
from .enum import side_enum


class JournalLine(db.Model):
    __tablename__ = "journal_lines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    journal_entry_id = Column(UUID(as_uuid=True), ForeignKey("journal_entries.id"), nullable=False)  # Buchungskopf
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)                # Konto
    amount = Column(Numeric, nullable=False)                                                          # Betrag
    side = Column(side_enum, nullable=False)                                                          # DEBIT / CREDIT

    tax_rate_id = Column(UUID(as_uuid=True), ForeignKey("tax_rates.id"), nullable=True)               # Optionaler Steuersatz
    cost_center_id = Column(UUID(as_uuid=True), ForeignKey("cost_centers.id"), nullable=True)         # Kostenstelle
    line_item_id = Column(UUID(as_uuid=True), ForeignKey("line_items.id"), nullable=True)             # Verknüpfte Belegposition
