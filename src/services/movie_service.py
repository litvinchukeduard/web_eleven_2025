from datetime import date

from sqlalchemy.orm import Session

from fastapi import HTTPException
from fastapi import status

from src.models import Movie
from src.repositories import movie_repository

def get_movie(movie_id: int, session: Session) -> Movie | None:
    movie_obj = session.get(Movie, movie_id)
    if movie_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id: '{movie_id}' not found")
    return movie_obj

def get_all_movies(session: Session) -> list[Movie]:
    return movie_repository.get_all_movies(session)

def create_movie(title: str, release_date: date, session: Session) -> Movie:
    db_movie = movie_repository.get_movie_by_title(title, session)
    if db_movie is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Movie with title: '{title}' already exists")
    return movie_repository.create(title, release_date, session)

def update_movie(movie_id: int, title: str, release_date: date, session: Session) -> Movie:
    movie_obj = get_movie(movie_id, session)
    movie_obj.title = title
    movie_obj.release_date = release_date
    return movie_repository.update(movie_obj, session)

def delete_movie(movie_id: int, session: Session) -> None:
    movie_obj = get_movie(movie_id, session)
    movie_repository.delete(movie_obj, session)
