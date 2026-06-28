import json
import redis
from app.core.config import settings
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)


def getCachedPrediction(key : str):
    value = redis_client.get(key)
    return eval(value) if value else None

def setCache(key : str, value : dict):
    redis_client.set(key, str(value))
    