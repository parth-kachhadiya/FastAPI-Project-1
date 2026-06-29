import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

try:
    if REDIS_URL.startswith("rediss://"):
        redis_client = redis.StrictRedis.from_url(
            REDIS_URL,
            decode_responses=True,
            ssl_cert_reqs=None    # only for SSL
        )
    else:
        redis_client = redis.StrictRedis.from_url(
            REDIS_URL,
            decode_responses=True  # plain connection, no SSL
        )
    redis_client.ping()
    REDIS_AVAILABLE = True
    print("[REDIS] Connected successfully!")
except Exception as e:
    redis_client = None
    REDIS_AVAILABLE = False
    print(f"[REDIS] Unavailable: {e}")

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