# app/schemas/auth.py
from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    role: str

class RefreshToken(BaseModel):
    refresh_token: str
