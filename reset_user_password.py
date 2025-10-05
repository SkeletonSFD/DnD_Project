"""
Скрипт для сброса пароля пользователя на Irina25011965
"""
import sys
from pathlib import Path

# Добавляем путь к backend в sys.path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.bd import Base, User
from app.crud import get_password_hash, get_user_by_username

# Создаем подключение к базе данных
DATABASE_URL = "sqlite:///./backend/dnd_app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def reset_password(username: str, new_password: str):
    """Сброс пароля пользователя"""
    db = SessionLocal()
    
    try:
        print(f"\n{'='*60}")
        print(f"СБРОС ПАРОЛЯ")
        print(f"{'='*60}")
        print(f"Username: {username}")
        print(f"New Password: {new_password}")
        
        # Получаем пользователя
        user = get_user_by_username(db, username)
        
        if not user:
            print(f"\n❌ ОШИБКА: Пользователь '{username}' не найден")
            return False
        
        print(f"\n✅ Пользователь найден:")
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        
        # Хешируем новый пароль
        new_hashed_password = get_password_hash(new_password)
        
        print(f"\n🔐 Хеширование нового пароля...")
        print(f"  Старый хеш: {user.hashed_password[:50]}...")
        print(f"  Новый хеш: {new_hashed_password[:50]}...")
        
        # Обновляем пароль
        user.hashed_password = new_hashed_password
        db.commit()
        
        print(f"\n✅ ПАРОЛЬ УСПЕШНО ИЗМЕНЕН!")
        print(f"\nТеперь вы можете войти с:")
        print(f"  Username: {username}")
        print(f"  Password: {new_password}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    # Сбрасываем пароль для SFDSkeleton на Irina25011965
    reset_password("SFDSkeleton", "Irina25011965")