from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.db.redis_config import redis_client

def ip_blacklist_middleware(app):
    @app.middleware("http")
    async def ip_blacklist(request: Request, call_next):
        client_ip = request.client.host
        key = f'blacklist:{client_ip}'
        if redis_client.get(key):
            return JSONResponse(content="IP is blocked", status_code=status.HTTP_403_FORBIDDEN)
        return await call_next(request)
    return ip_blacklist
