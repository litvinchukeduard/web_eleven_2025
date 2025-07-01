from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from src.schemas.movie import MovieRequest, MovieResponse
from src.schemas.movie_rating import MovieRatingRequest
from src.schemas.movie_rating import MovieRatingResponse
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
    movie_obj, avg_rating = movie_service.get_movie(movie_id, session)
    movie_response = MovieResponse.model_validate(movie_obj)
    movie_response.average_rating = avg_rating
    return movie_response

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

@router.post("/movies/{movie_id}/add_rating", response_model=MovieRatingResponse)
def add_rating_to_movie(movie_id: int, movie_rating: MovieRatingRequest, session: Session = Depends(open_session)):
    movie_rating = movie_service.add_movie_rating(movie_id, movie_rating.movie_rating, session)
    return MovieRatingResponse.model_validate(movie_rating)
