import os
from dotenv import load_dotenv


load_dotenv()


class Setting:
    PROJECT_NAME = "Car Price API"
    API_KEY = os.getenv(
        'API_KEY',
        'backup_key-werjiodEHR45UE'       # In case of no 'API_KEY' found from .env file, use this as API_KEY
    )
    JWT_SECRET_KEY = os.getenv(
        'JWT_SECRET_KEY',
        'backup_key-rlgjlSLEJ445JJ'
    )
    JWT_ALGO = "HS256"
    REDIS_URL = os.getenv(
        'REDIS_URL',
        'redis://localhost:6379'
    )
    MODEL_LOCATION = "app\\models\\model.pkl"

settings = Setting()