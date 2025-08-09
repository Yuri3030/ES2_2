from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, conint
from datetime import datetime

# Modelo para entrada de cadastro
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Modelo para resposta (não retorna a senha)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


# Modelo para login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Modelo para resposta de login
class LoginResponse(BaseModel):
    message: str
    token: str | None = None  


class MoodCreate(BaseModel):
    score: conint(ge=1, le=5)
    comment: str | None = None

class MoodResponse(BaseModel):
    id: int
    score: int
    comment: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
