from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, ForeignKey
from . import db

document_tag = Table(
    'document_tag',
    db.Model.metadata,
    Column('document_id', UUID(as_uuid=True), ForeignKey('document.id'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tag.id'), primary_key=True)
)