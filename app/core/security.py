from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from app.core.config import Settings


def createToken(data : dict, expire_in_minutes=30):
    copy_of_data = data.copy()
    expire_in = datetime.now(timezone.utc) + timedelta(minutes=expire_in_minutes)
    copy_of_data.update({'expiry' : expire_in })

    return jwt.encode(
        copy_of_data,
        key = Settings.JWT_SECRET_KEY,
        algorithm = Settings.JWT_ALGO
    )

def tokenVerification(token : str):
    try:
        payload = jwt.decode(
            token,
            key = Settings.JWT_SECRET_KEY,
            algorithms = [Settings.JWT_ALGO]
        )
        return payload
    except JWTError:
        return None