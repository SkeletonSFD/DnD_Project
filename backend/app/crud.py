from sqlalchemy.orm import Session
from app.bd import User
import bcrypt
from typing import Optional


def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    # Bcrypt имеет ограничение в 72 байта
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    # Bcrypt имеет ограничение в 72 байта
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Получить пользователя по имени пользователя"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Получить пользователя по email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Получить пользователя по ID"""
    return db.query(User).filter(User.id == user_id).first()


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str,
    character_name: Optional[str] = None
) -> User:
    """
    Создать нового пользователя
    
    Args:
        db: Сессия базы данных
        username: Имя пользователя
        email: Email пользователя
        password: Пароль (будет захеширован)
        character_name: Имя персонажа (опционально)
    
    Returns:
        User: Созданный пользователь
    """
    hashed_password = get_password_hash(password)
    
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        character_name=character_name,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Аутентификация пользователя
    
    Args:
        db: Сессия базы данных
        username: Имя пользователя или email
        password: Пароль
    
    Returns:
        User: Пользователь, если аутентификация успешна, иначе None
    """
    # Попытка найти по username
    user = get_user_by_username(db, username)
    
    # Если не найден, попытка найти по email
    if not user:
        user = get_user_by_email(db, username)
    
    # Проверка пароля
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user


def update_user(
    db: Session,
    user_id: int,
    username: Optional[str] = None,
    email: Optional[str] = None,
    character_name: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Optional[User]:
    """
    Обновить данные пользователя
    
    Args:
        db: Сессия базы данных
        user_id: ID пользователя
        username: Новое имя пользователя (опционально)
        email: Новый email (опционально)
        character_name: Новое имя персонажа (опционально)
        is_active: Новый статус активности (опционально)
    
    Returns:
        User: Обновленный пользователь или None, если не найден
    """
    user = get_user_by_id(db, user_id)
    
    if not user:
        return None
    
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if character_name is not None:
        user.character_name = character_name
    if is_active is not None:
        user.is_active = is_active
    
    db.commit()
    db.refresh(user)
    
    return user


def delete_user(db: Session, user_id: int) -> bool:
    """
    Удалить пользователя
    
    Args:
        db: Сессия базы данных
        user_id: ID пользователя
    
    Returns:
        bool: True, если пользователь удален, иначе False
    """
    user = get_user_by_id(db, user_id)
    
    if not user:
        return False
    
    db.delete(user)
    db.commit()
    
    return True


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить список всех пользователей
    
    Args:
        db: Сессия базы данных
        skip: Количество пропускаемых записей
        limit: Максимальное количество возвращаемых записей
    
    Returns:
        List[User]: Список пользователей
    """
    return db.query(User).offset(skip).limit(limit).all()