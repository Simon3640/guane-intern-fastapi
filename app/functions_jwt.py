from datetime import datetime, timedelta
from jwt import encode, decode, exceptions
from os import getenv
from fastapi.responses import JSONResponse


#Esta dunción nos ayuda a setear cuánto tiempo dura el token
def expire_token(days: int): 
    date = datetime.now() + timedelta(days=days)
    return date


#Esta dunción nos ayuda a generar el token
def write_token(data: dict):
    token = encode(payload={**data, 'exp': expire_token(20)}, key=getenv("SECRET"), algorithm='HS256')
    return token


#Esta dunción nos ayuda a leer el token
def validate_token(token: str, output = False):
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=['HS256'])
        else:
            decode(token, key=getenv("SECRET"), algorithms=['HS256'])
    except exceptions.DecodeError:
        return JSONResponse(status_code=401, content={"message": "Invalid token"})
    except exceptions.ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"message": "Token expired"})