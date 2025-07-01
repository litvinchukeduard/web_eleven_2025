from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models import MovieRating

def add_rating(movie_id: int, rating: int, session: Session) -> MovieRating:
    movie_rating_obj = MovieRating(movie_id=movie_id, movie_rating=rating)
    session.add(movie_rating_obj)
    session.commit()
    return movie_rating_obj

'''
SELECT avg(mr.movie_rating) FROM movie_ratings mr
WHERE movie_id = 1;
'''
# TODO: !important Actually use select!
def get_average_rating(movie_id: int, session: Session) -> float:
    return session.query(func.avg(MovieRating.movie_rating)).filter(MovieRating.movie_id == movie_id).scalar()
