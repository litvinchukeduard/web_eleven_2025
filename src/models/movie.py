from datetime import date

from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db.base import Base


class Movie(Base):
    __tablename__ = "movies"
    __table_args__ = (
        UniqueConstraint("title", name="unique_movie_title"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    release_date: Mapped[date] = mapped_column(Date, default=lambda: date(1980, 1, 1), server_default="1980-01-01")
    
    def __repr__(self) -> str:
        return f"Movie(id={self.id!r}, title={self.title!r})"
    