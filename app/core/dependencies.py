from fastapi import Header, HTTPException
from app.core.config import settings
from app.core.security import tokenVerification



def getAPIKey(api_key : str = Header(...)):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code = 403,
            detail = "Invalid API Key..!"
        )


def getCurrentUser(token : str = Header(...)):
    payload = tokenVerification(token)
    if not payload:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid JWT Token..!"
        )

    return payload

