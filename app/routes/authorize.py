from fastapi import APIRouter, Header
from functions_jwt import validate_token

from functions_jwt import write_token

Route=APIRouter()

@Route.post(
    "/auth",
    response_model=str,
    summary="Authorize user",
    tags=["authorize"]
    )
def login():
    return write_token({"name": "Guane"}) #! Esto genera un token sin verificar nada
