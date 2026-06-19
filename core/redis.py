from redis.asyncio import Redis
from config.config import redis_settings

redis = Redis(
    port=redis_settings.REDIS_PORT,
    db=redis_settings.REDIS_DATABASE,
    password=redis_settings.REDIS_PASSWORD,
    host=redis_settings.REDIS_HOST,
    username=redis_settings.REDIS_USERNAME
        )