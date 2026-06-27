from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from app.core.config import settings


def createToken(data, expire_in_minutes=30):
    if hasattr(data, "model_dump"):
        copy_of_data = data.model_dump()
    elif hasattr(data, "dict"):
        copy_of_data = data.dict()
    else:
        copy_of_data = dict(data)
        
    expire_in = datetime.now(timezone.utc) + timedelta(minutes=expire_in_minutes)
    copy_of_data.update({'exp' : expire_in })

    return jwt.encode(
        copy_of_data,
        key = settings.JWT_SECRET_KEY,
        algorithm = settings.JWT_ALGO
    )

def tokenVerification(token : str):
    try:
        payload = jwt.decode(
            token,
            key = settings.JWT_SECRET_KEY,
            algorithms = [settings.JWT_ALGO]
        )
        return payload
    except JWTError:
        return None