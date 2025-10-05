"""
Тестовый скрипт для проверки работы базы данных
"""
from bd import SessionLocal, init_db
from crud import (
    create_user, 
    get_user_by_username, 
    authenticate_user,
    get_all_users
)

def test_database():
    """Тестирование основных операций с базой данных"""
    
    print("=" * 60)
    print("🧪 ТЕСТИРОВАНИЕ БАЗЫ ДАННЫХ D&D ПРИЛОЖЕНИЯ")
    print("=" * 60)
    
    # Инициализация БД
    print("\n1️⃣ Инициализация базы данных...")
    init_db()
    
    # Создание сессии
    db = SessionLocal()
    
    try:
        # Тест 1: Создание пользователя
        print("\n2️⃣ Создание тестового пользователя...")
        test_username = "test_wizard"
        test_email = "wizard@dnd.com"
        test_password = "MagicPass123"
        
        # Проверка, существует ли уже пользователь
        existing_user = get_user_by_username(db, test_username)
        if existing_user:
            print(f"   ⚠️  Пользователь '{test_username}' уже существует")
        else:
            user = create_user(
                db=db,
                username=test_username,
                email=test_email,
                password=test_password,
                character_name="Гэндальф Серый"
            )
            print(f"   ✅ Пользователь создан: {user.username} (ID: {user.id})")
            print(f"   📧 Email: {user.email}")
            print(f"   🎭 Персонаж: {user.character_name}")
        
        # Тест 2: Получение пользователя
        print("\n3️⃣ Получение пользователя из базы данных...")
        user = get_user_by_username(db, test_username)
        if user:
            print(f"   ✅ Пользователь найден: {user.username}")
            print(f"   📅 Создан: {user.created_at}")
            print(f"   🟢 Активен: {user.is_active}")
        else:
            print(f"   ❌ Пользователь не найден")
        
        # Тест 3: Аутентификация
        print("\n4️⃣ Тестирование аутентификации...")
        
        # Правильный пароль
        auth_user = authenticate_user(db, test_username, test_password)
        if auth_user:
            print(f"   ✅ Аутентификация успешна для: {auth_user.username}")
        else:
            print(f"   ❌ Аутентификация не удалась")
        
        # Неправильный пароль
        wrong_auth = authenticate_user(db, test_username, "WrongPassword123")
        if wrong_auth:
            print(f"   ❌ ОШИБКА: Аутентификация прошла с неверным паролем!")
        else:
            print(f"   ✅ Неверный пароль корректно отклонен")
        
        # Тест 4: Список всех пользователей
        print("\n5️⃣ Получение списка всех пользователей...")
        all_users = get_all_users(db)
        print(f"   📊 Всего пользователей в базе: {len(all_users)}")
        for idx, u in enumerate(all_users, 1):
            print(f"   {idx}. {u.username} ({u.email}) - {u.character_name or 'без персонажа'}")
        
        print("\n" + "=" * 60)
        print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ УСПЕШНО!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()
        print("\n🔒 Соединение с базой данных закрыто")


if __name__ == "__main__":
    test_database()