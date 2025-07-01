from pydantic import BaseModel, ConfigDict, field_validator


class MovieRatingRequest(BaseModel):
    movie_rating: int

    @field_validator('movie_rating', mode='after')
    @classmethod
    def ensure_movie_rating_is_within_boundaries(cls, v: int):
        if not 1 <= v <= 5:
            raise ValueError("Movie Rating should be between 1 and 5")
        return v


class MovieRatingResponse(BaseModel):
    id: int
    movie_id: int
    movie_rating: int

    model_config = ConfigDict(from_attributes=True)
