"""
Скрипт для отладки аутентификации
"""
import sys
from pathlib import Path

# Добавляем путь к backend в sys.path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.bd import Base, User
from app.crud import authenticate_user, verify_password, get_user_by_username
import bcrypt

# Создаем подключение к базе данных
DATABASE_URL = "sqlite:///./backend/dnd_app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def debug_user_auth(username: str, password: str):
    """Отладка аутентификации пользователя"""
    db = SessionLocal()
    
    try:
        print(f"\n{'='*60}")
        print(f"ОТЛАДКА АУТЕНТИФИКАЦИИ")
        print(f"{'='*60}")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Password length: {len(password)} символов")
        print(f"Password bytes: {len(password.encode('utf-8'))} байт")
        
        # Получаем пользователя
        user = get_user_by_username(db, username)
        
        if not user:
            print(f"\n❌ ОШИБКА: Пользователь '{username}' не найден в базе данных")
            print("\nСписок всех пользователей:")
            all_users = db.query(User).all()
            for u in all_users:
                print(f"  - {u.username} (ID: {u.id}, Email: {u.email})")
            return False
        
        print(f"\n✅ Пользователь найден:")
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Character Name: {user.character_name}")
        print(f"  Is Active: {user.is_active}")
        print(f"  Hashed Password: {user.hashed_password[:50]}...")
        
        # Проверяем пароль
        print(f"\n{'='*60}")
        print(f"ПРОВЕРКА ПАРОЛЯ")
        print(f"{'='*60}")
        
        # Ручная проверка bcrypt
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
            print(f"⚠️  Пароль обрезан до 72 байт")
        
        hashed_bytes = user.hashed_password.encode('utf-8')
        
        try:
            result = bcrypt.checkpw(password_bytes, hashed_bytes)
            print(f"\nРезультат bcrypt.checkpw: {result}")
            
            if result:
                print(f"✅ ПАРОЛЬ ВЕРНЫЙ!")
            else:
                print(f"❌ ПАРОЛЬ НЕВЕРНЫЙ!")
                
                # Попробуем разные варианты
                print(f"\nПопытка проверки с разными вариантами:")
                
                # Вариант 1: без обрезки
                try:
                    result1 = bcrypt.checkpw(password.encode('utf-8'), hashed_bytes)
                    print(f"  Без обрезки: {result1}")
                except Exception as e:
                    print(f"  Без обрезки: Ошибка - {e}")
                
                # Вариант 2: с пробелами
                try:
                    result2 = bcrypt.checkpw(f" {password}".encode('utf-8')[:72], hashed_bytes)
                    print(f"  С пробелом в начале: {result2}")
                except Exception as e:
                    print(f"  С пробелом в начале: Ошибка - {e}")
                
                try:
                    result3 = bcrypt.checkpw(f"{password} ".encode('utf-8')[:72], hashed_bytes)
                    print(f"  С пробелом в конце: {result3}")
                except Exception as e:
                    print(f"  С пробелом в конце: Ошибка - {e}")
                
        except Exception as e:
            print(f"❌ ОШИБКА при проверке пароля: {e}")
            return False
        
        # Проверяем через функцию verify_password
        print(f"\n{'='*60}")
        print(f"ПРОВЕРКА ЧЕРЕЗ verify_password()")
        print(f"{'='*60}")
        
        verify_result = verify_password(password, user.hashed_password)
        print(f"Результат: {verify_result}")
        
        # Проверяем через authenticate_user
        print(f"\n{'='*60}")
        print(f"ПРОВЕРКА ЧЕРЕЗ authenticate_user()")
        print(f"{'='*60}")
        
        auth_user = authenticate_user(db, username, password)
        if auth_user:
            print(f"✅ АУТЕНТИФИКАЦИЯ УСПЕШНА!")
            print(f"  User ID: {auth_user.id}")
            print(f"  Username: {auth_user.username}")
            return True
        else:
            print(f"❌ АУТЕНТИФИКАЦИЯ ПРОВАЛИЛАСЬ!")
            return False
            
    finally:
        db.close()


def list_all_users():
    """Список всех пользователей"""
    db = SessionLocal()
    
    try:
        print(f"\n{'='*60}")
        print(f"ВСЕ ПОЛЬЗОВАТЕЛИ В БАЗЕ ДАННЫХ")
        print(f"{'='*60}")
        
        users = db.query(User).all()
        
        if not users:
            print("База данных пуста")
            return
        
        for user in users:
            print(f"\nПользователь #{user.id}:")
            print(f"  Username: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Character Name: {user.character_name}")
            print(f"  Is Active: {user.is_active}")
            print(f"  Hashed Password: {user.hashed_password[:50]}...")
            
    finally:
        db.close()


if __name__ == "__main__":
    # Сначала показываем всех пользователей
    list_all_users()
    
    # Тестируем аутентификацию
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ АУТЕНТИФИКАЦИИ")
    print("="*60)
    
    # Тест 1: SFDSkeleton
    debug_user_auth("SFDSkeleton", "Password123")
    
    # Тест 2: TestUser123
    print("\n")
    debug_user_auth("TestUser123", "Password123")