import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

try:
    import redis
    redis_client = redis.StrictRedis.from_url(
        REDIS_URL,
        decode_responses=True,
        username=None,    # ✅ no auth for local
        password=None     # ✅ no auth for local
    )
    redis_client.ping()
    REDIS_AVAILABLE = True
except Exception:
    redis_client = None
    REDIS_AVAILABLE = False

def getCachedPrediction(key: str):
    if not REDIS_AVAILABLE:
        return None
    try:
        value = redis_client.get(key)
        return eval(value) if value else None
    except Exception:
        return None

def setCache(key: str, value: dict):
    if not REDIS_AVAILABLE:
        return
    try:
        redis_client.set(key, str(value))
    except Exception:
        pass