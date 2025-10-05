"""
Тестовый скрипт для проверки аутентификации
"""
import sys
sys.path.insert(0, 'backend')

from app.bd import SessionLocal
from app.crud import authenticate_user, get_user_by_username

# Создаем сессию
db = SessionLocal()

# Тестируем пользователя
username = "SFDSkeleton"
test_passwords = [
    "Password123",
    "password123",
    "PASSWORD123",
    "Password1",
    "Password12",
]

print(f"🔍 Проверка пользователя: {username}\n")

# Проверяем, существует ли пользователь
user = get_user_by_username(db, username)
if user:
    print(f"✅ Пользователь найден:")
    print(f"   ID: {user.id}")
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Active: {user.is_active}")
    print(f"   Hashed password (first 50 chars): {user.hashed_password[:50]}...")
    print()
    
    print("🔐 Тестирование паролей:")
    for password in test_passwords:
        result = authenticate_user(db, username, password)
        status = "✅ УСПЕХ" if result else "❌ НЕУДАЧА"
        print(f"   {status}: '{password}'")
else:
    print(f"❌ Пользователь '{username}' не найден в базе данных")

db.close()

print("\n" + "="*60)
print("💡 Подсказка:")
print("   Если все пароли не подходят, возможно пользователь был")
print("   зарегистрирован с другим паролем или произошла ошибка")
print("   при хешировании.")
print("="*60)