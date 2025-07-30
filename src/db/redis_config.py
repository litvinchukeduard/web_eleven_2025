import redis 

from src.config.app_config import app_settings

redis_client = redis.Redis.from_url(
    app_settings.REDIS_CONNECT_URL,
    decode_responses=True
)
