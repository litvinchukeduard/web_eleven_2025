import uvicorn
from fastapi import FastAPI

from src.api.movie_api import router as movie_router
from src.api.user_api import router as user_router

from src.middleware.hello_world_middleware import hello_middleware
from src.middleware.ip_blacklist_middleware import ip_blacklist_middleware

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Movie rating API is working"}

app.include_router(movie_router)
app.include_router(user_router)

hello_middleware(app)
ip_blacklist_middleware(app)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
