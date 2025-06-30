import uvicorn

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status

from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from pydantic import BaseModel, ConfigDict


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"
    __table_args__ = (
        UniqueConstraint("title", name="unique_movie_title"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    
    def __repr__(self) -> str:
        return f"Movie(id={self.id!r}, title={self.title!r})"
    

class MovieRequest(BaseModel):
    title: str


class MovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str

DATABASE_CONNECT_URL = "sqlite:///movies_app.db"

engine = create_engine(
    DATABASE_CONNECT_URL, connect_args={"autocommit": False}
)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Movie rating API is working"}

# Create a Movie and store in db
@app.post("/movies/", response_model=MovieResponse)
def create_movie(movie: MovieRequest):
    with Session(engine) as session:
        db_movie = session.query(Movie).filter(Movie.title == movie.title)
        if db_movie is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Movie with title: '{movie.title}' already exists")

        movie_obj = Movie(title=movie.title)
        session.add(movie_obj)
        session.commit()
        return MovieResponse.model_validate(movie_obj)
    
# Get one Movie from db
@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int):
    with Session(engine) as session:
        movie_obj = session.get(Movie, movie_id)
        if movie_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id: '{movie_id}' not found")
        return MovieResponse.model_validate(session.get(Movie, movie_id))

# Get all movies from db
@app.get("/movies/", response_model=list[MovieResponse])
def get_all_movies():
    with Session(engine) as session:
        movies = session.query(Movie).all()
        return [MovieResponse.model_validate(m) for m in movies]

# Update a Movie in db
@app.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie: MovieRequest):
    with Session(engine) as session:
        movie_obj = session.get(Movie, movie_id)
        if movie_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id: '{movie_id}' not found")
        
        movie_obj.title = movie.title
        session.commit()

        return MovieResponse.model_validate(movie_obj)



# Delete a Movie in db
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    with Session(engine) as session:
        movie_obj = session.get(Movie, movie_id)
        if movie_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id: '{movie_id}' not found")
        
        session.delete(movie_obj)
        session.commit()

        return {'message': f'Movie with id "{movie_id}" deleted successfully'}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)