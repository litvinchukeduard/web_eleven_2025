import uvicorn
from fastapi import FastAPI

from src.api.movie_api import router as movie_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Movie rating API is working"}

app.include_router(movie_router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)