import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent  # /app/app

class Setting:
    PROJECT_NAME = "Car Price API"
    API_KEY = os.getenv('API_KEY', 'backup_key-werjiodEHR45UE')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'backup_key-rlgjlSLEJ445JJ')
    JWT_ALGO = "HS256"
    REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379')  
    MODEL_LOCATION = BASE_DIR / "models" / "xgb_model.pkl"       
    PREPROCESSOR_LOCATION = BASE_DIR / "models" / "preprocessor.pkl" 

settings = Setting()