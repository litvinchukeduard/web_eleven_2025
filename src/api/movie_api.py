from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends

from sqlalchemy.orm import Session

from src.schemas.movie import MovieRequest, MovieResponse
from src.db.session import open_session
from src.models.movie import Movie

router = APIRouter()

# Create a Movie and store in db
@router.post("/movies/", response_model=MovieResponse)
def create_movie(movie: MovieRequest, session: Session = Depends(open_session)):
    db_movie = session.query(Movie).filter(Movie.title == movie.title).first()
    if db_movie is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Movie with title: '{movie.title}' already exists")

    movie_obj = Movie(title=movie.title, release_date=movie.release_date)
    session.add(movie_obj)
    session.commit()
    return MovieResponse.model_validate(movie_obj)
    
# Get one Movie from db
@router.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, session: Session = Depends(open_session)):
    movie_obj = session.get(Movie, movie_id)
    if movie_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id: '{movie_id}' not found")
    return MovieResponse.model_validate(session.get(Movie, movie_id))

# Get all movies from db
@router.get("/movies/", response_model=list[MovieResponse])
def get_all_movies(session: Session = Depends(open_session)):
    movies = session.query(Movie).all()
    return [MovieResponse.model_validate(m) for m in movies]

# Update a Movie in db
@router.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie: MovieRequest, session: Session = Depends(open_session)):
    movie_obj = session.get(Movie, movie_id)
    if movie_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id: '{movie_id}' not found")
    
    movie_obj.title = movie.title
    session.commit()

    return MovieResponse.model_validate(movie_obj)

# Delete a Movie in db
@router.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, session: Session = Depends(open_session)):
    movie_obj = session.get(Movie, movie_id)
    if movie_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id: '{movie_id}' not found")
    
    session.delete(movie_obj)
    session.commit()

    return {'message': f'Movie with id "{movie_id}" deleted successfully'}
