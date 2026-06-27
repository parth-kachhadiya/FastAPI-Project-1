import json
import redis
from app.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL)


def getCachedPrediction(key : str):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def setCache(key : str, value : dict, expiry_in_minute : int = 10):
    redis_client.setex(key, json.dumps(value))
    