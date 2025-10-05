"""
Тестовый скрипт для проверки регистрации и входа
"""
import sys
sys.path.insert(0, 'backend')

from app.bd import SessionLocal
from app.crud import create_user, authenticate_user, get_user_by_username

# Создаем сессию
db = SessionLocal()

# Тестовые данные
test_username = "TestUser123"
test_email = "testuser123@example.com"
test_password = "Password123"

print("🧪 Тест регистрации и аутентификации\n")
print("="*60)

# Проверяем, существует ли пользователь
existing_user = get_user_by_username(db, test_username)
if existing_user:
    print(f"⚠️  Пользователь '{test_username}' уже существует")
    print(f"   Используем существующего пользователя для теста\n")
    user = existing_user
else:
    print(f"📝 Создание нового пользователя:")
    print(f"   Username: {test_username}")
    print(f"   Email: {test_email}")
    print(f"   Password: {test_password}")
    
    try:
        user = create_user(
            db=db,
            username=test_username,
            email=test_email,
            password=test_password,
            character_name="Test Character"
        )
        print(f"✅ Пользователь успешно создан (ID: {user.id})\n")
    except Exception as e:
        print(f"❌ Ошибка при создании пользователя: {e}")
        db.close()
        sys.exit(1)

# Тестируем аутентификацию
print("="*60)
print("🔐 Тест аутентификации:")
print(f"   Username: {test_username}")
print(f"   Password: {test_password}")

auth_result = authenticate_user(db, test_username, test_password)

if auth_result:
    print(f"✅ УСПЕХ! Аутентификация прошла успешно")
    print(f"   User ID: {auth_result.id}")
    print(f"   Username: {auth_result.username}")
    print(f"   Email: {auth_result.email}")
else:
    print(f"❌ НЕУДАЧА! Аутентификация не прошла")
    print(f"   Проверьте правильность пароля")

db.close()

print("="*60)
print("\n💡 Результат:")
if auth_result:
    print(f"   ✅ Регистрация и вход работают корректно!")
    print(f"   Используйте эти данные для входа:")
    print(f"   Username: {test_username}")
    print(f"   Password: {test_password}")
else:
    print(f"   ❌ Есть проблема с хешированием/проверкой пароля")