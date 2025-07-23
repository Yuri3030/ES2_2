from pydantic import BaseModel, EmailStr

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
