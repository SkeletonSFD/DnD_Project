"""
Проверка пароля Irina25011965 для пользователя SFDSkeleton
"""
import sys
import os

# Добавляем путь к backend
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Устанавливаем переменную окружения для базы данных
os.environ['DATABASE_URL'] = 'sqlite:///./dnd_app.db'

from backend.app.database import SessionLocal
from backend.app.models import User
from backend.app.auth import verify_password
import bcrypt

def check_password():
    db = SessionLocal()
    try:
        # Получаем пользователя
        user = db.query(User).filter(User.username == "SFDSkeleton").first()
        
        if not user:
            print("❌ Пользователь SFDSkeleton не найден!")
            return
        
        print(f"✅ Пользователь найден:")
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Hashed Password: {user.hashed_password[:60]}...")
        print()
        
        # Проверяем разные пароли
        passwords_to_test = [
            "Irina25011965",
            "Password123",
            "irina25011965",
            "IRINA25011965"
        ]
        
        print("=" * 60)
        print("ПРОВЕРКА ПАРОЛЕЙ")
        print("=" * 60)
        
        for password in passwords_to_test:
            print(f"\nПроверка пароля: {password}")
            
            # Прямая проверка bcrypt
            try:
                result = bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password.encode('utf-8')
                )
                print(f"  bcrypt.checkpw: {result}")
                
                if result:
                    print(f"  ✅ ПАРОЛЬ ВЕРНЫЙ: {password}")
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
            
            # Проверка через verify_password
            result2 = verify_password(password, user.hashed_password)
            print(f"  verify_password: {result2}")
            
            if result2:
                print(f"  ✅ ПАРОЛЬ ВЕРНЫЙ (verify_password): {password}")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_password()