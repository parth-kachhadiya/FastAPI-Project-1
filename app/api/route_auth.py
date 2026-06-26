from fastapi import APIRouter
from pydantic import BaseModel
from app.core.security import createToken


router = APIRouter()

class AuthDataModel(BaseModel):
    username : str
    password : str



@router.post('/auth')
def doAuthentication(data : AuthDataModel):
    if data.username == 'admin' and data.password == 'admin':
        token = createToken(data)
        return {'token' : token }
    return {'error' : 'Invalid credentials..!' }
