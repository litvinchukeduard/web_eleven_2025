from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.db.base import Base

'''
Movie -> MovieRating
'''

class MovieRating(Base):
    __tablename__ = "movie_ratings"

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    movie_rating:  Mapped[int] = mapped_column()
    movie: Mapped["Movie"] = relationship()
