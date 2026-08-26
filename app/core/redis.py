import redis
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Shared Redis instance for caching
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

# Shared Slowapi limiter instance for rate limiting backed by Redis
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.REDIS_URL
)
