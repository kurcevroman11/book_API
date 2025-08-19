from sqlalchemy import Table, Column, Integer, String, JSON
from app.core.database import metadata

books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("author", String, nullable=False),
    Column("publish_year", Integer, nullable=False),
    Column("genres", JSON, nullable=False),
    Column("rating", Integer, nullable=False)
)