"""
Скрипт для сброса пароля пользователя
"""
import sys
sys.path.insert(0, 'backend')

from app.bd import SessionLocal
from app.crud import get_user_by_username, get_password_hash

# Создаем сессию
db = SessionLocal()

# Данные для сброса
username = "SFDSkeleton"
new_password = "Password123"

print("🔐 Сброс пароля пользователя\n")
print("="*60)

# Находим пользователя
user = get_user_by_username(db, username)

if not user:
    print(f"❌ Пользователь '{username}' не найден")
    db.close()
    sys.exit(1)

print(f"✅ Пользователь найден:")
print(f"   ID: {user.id}")
print(f"   Username: {user.username}")
print(f"   Email: {user.email}")
print()

# Хешируем новый пароль
print(f"🔄 Установка нового пароля: {new_password}")
new_hashed_password = get_password_hash(new_password)

# Обновляем пароль
user.hashed_password = new_hashed_password
db.commit()

print(f"✅ Пароль успешно обновлен!")
print()
print("="*60)
print("💡 Теперь вы можете войти с этими данными:")
print(f"   Username: {username}")
print(f"   Password: {new_password}")
print("="*60)

db.close()