from sqlalchemy import func, select
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
def get_average_rating(movie_id: int, session: Session) -> float:
    select_statement = select(func.avg(MovieRating.movie_rating)).where(MovieRating.movie_id == movie_id)
    return session.execute(select_statement).scalar_one()
