from datetime import date

from pydantic import BaseModel, ConfigDict


class MovieRequest(BaseModel):
    title: str
    release_date: date


class MovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    release_date: date
    average_rating: float | None = None
