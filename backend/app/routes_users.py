"""
Роуты для работы с пользователями
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.bd import get_db, User
from app.crud import (
    create_user,
    get_user_by_username,
    get_user_by_email,
    authenticate_user,
    get_all_users
)
from app.schemas import (
    UserRegistrationRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse
)
from app.auth import create_access_token, get_current_active_user
from datetime import timedelta

router = APIRouter(prefix="/api/users", tags=["Пользователи"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegistrationRequest,
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя
    
    - **username**: Имя пользователя (3-50 символов, только буквы, цифры, дефисы и подчеркивания)
    - **email**: Email пользователя
    - **password**: Пароль (минимум 8 символов, должен содержать цифры, заглавные и строчные буквы)
    - **confirm_password**: Подтверждение пароля
    - **character_name**: Имя персонажа (опционально)
    """
    # Проверка существования пользователя с таким username
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )
    
    # Проверка существования пользователя с таким email
    existing_email = get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    
    try:
        # Создание пользователя
        new_user = create_user(
            db=db,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            character_name=user_data.character_name
        )
        
        # Создание токена доступа
        access_token = create_access_token(
            data={"sub": str(new_user.id)},
            expires_delta=timedelta(days=1)
        )
        
        # Формирование ответа
        user_response = UserResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            character_name=new_user.character_name,
            is_active=new_user.is_active
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при создании пользователя"
        )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Вход пользователя в систему (OAuth2 совместимый)
    
    - **username**: Имя пользователя или email
    - **password**: Пароль
    """
    # Аутентификация пользователя
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь неактивен"
        )
    
    # Создание токена доступа
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=1)
    )
    
    # Формирование ответа
    user_response = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        character_name=user.character_name,
        is_active=user.is_active
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Получение информации о текущем пользователе
    
    Требуется авторизация (Bearer токен)
    """
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        character_name=current_user.character_name,
        is_active=current_user.is_active
    )


@router.get("/", response_model=list[UserResponse])
async def get_users_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Получение списка всех пользователей
    
    Требуется авторизация (Bearer токен)
    
    - **skip**: Количество пропускаемых записей (для пагинации)
    - **limit**: Максимальное количество возвращаемых записей
    """
    users = get_all_users(db, skip=skip, limit=limit)
    
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            character_name=user.character_name,
            is_active=user.is_active
        )
        for user in users
    ]