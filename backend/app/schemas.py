from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class UserRegistrationRequest(BaseModel):
    """Модель запроса для регистрации нового пользователя"""
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=8, max_length=100, description="Пароль пользователя")
    confirm_password: str = Field(..., min_length=8, max_length=100, description="Подтверждение пароля")
    character_name: Optional[str] = Field(None, max_length=100, description="Имя персонажа (опционально)")
    
    @validator('username')
    def validate_username(cls, v):
        """Проверка имени пользователя"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Имя пользователя может содержать только буквы, цифры, дефисы и подчеркивания')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        """Проверка сложности пароля"""
        if not any(char.isdigit() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not any(char.isupper() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not any(char.islower() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Проверка совпадения паролей"""
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "dungeon_master",
                "email": "dm@example.com",
                "password": "SecurePass123",
                "confirm_password": "SecurePass123",
                "character_name": "Арагорн"
            }
        }


class UserLoginRequest(BaseModel):
    """Модель запроса для входа пользователя"""
    username: str = Field(..., description="Имя пользователя или email")
    password: str = Field(..., description="Пароль пользователя")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "dungeon_master",
                "password": "SecurePass123"
            }
        }


class UserResponse(BaseModel):
    """Модель ответа с данными пользователя"""
    id: int
    username: str
    email: str
    character_name: Optional[str] = None
    is_active: bool = True
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "dungeon_master",
                "email": "dm@example.com",
                "character_name": "Арагорн",
                "is_active": True
            }
        }


class TokenResponse(BaseModel):
    """Модель ответа с токеном доступа"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "username": "dungeon_master",
                    "email": "dm@example.com",
                    "character_name": "Арагорн",
                    "is_active": True
                }
            }
        }