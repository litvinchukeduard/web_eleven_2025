from datetime import date

from sqlalchemy.orm import Session

from src.models import Movie

def get_movie(movie_id: int, session: Session) -> Movie | None:
    return session.get(Movie, movie_id)

def get_movie_by_title(movie_title: str, session: Session) -> Movie | None:
    return session.query(Movie).filter(Movie.title == movie_title).first()

def get_all_movies(session: Session) -> list[Movie]:
    return session.query(Movie).all()

def create(title: str, release_date: date, session: Session) -> Movie:
    movie_obj = Movie(title=title, release_date=release_date)
    session.add(movie_obj)
    session.commit()
    return movie_obj

def update(movie: Movie, session: Session) -> Movie:
    session.add(movie)
    session.commit()
    return movie

def delete(movie: Movie, session: Session) -> None:
    session.delete(movie)
    session.commit()
