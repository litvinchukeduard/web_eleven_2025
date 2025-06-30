from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from src.schemas.movie import MovieRequest, MovieResponse
from src.db.session import open_session
from src.services import movie_service

router = APIRouter()

# Create a Movie and store in db
@router.post("/movies/", response_model=MovieResponse)
def create_movie(movie: MovieRequest, session: Session = Depends(open_session)):
    movie_obj = movie_service.create_movie(movie.title, movie.release_date, session)
    return MovieResponse.model_validate(movie_obj)
    
# Get one Movie from db
@router.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, session: Session = Depends(open_session)):
    movie_obj = movie_service.get_movie(movie_id, session)
    return MovieResponse.model_validate(movie_obj)

# Get all movies from db
@router.get("/movies/", response_model=list[MovieResponse])
def get_all_movies(session: Session = Depends(open_session)):
    movies = movie_service.get_all_movies(session)
    return [MovieResponse.model_validate(m) for m in movies]

# Update a Movie in db
@router.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie: MovieRequest, session: Session = Depends(open_session)):
    movie_obj = movie_service.update_movie(movie_id, movie.title, movie.release_date, session)
    return MovieResponse.model_validate(movie_obj)

# Delete a Movie in db
@router.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, session: Session = Depends(open_session)):
    movie_service.delete_movie(movie_id, session)
    return {'message': f'Movie with id "{movie_id}" deleted successfully'}
