"""
Быстрый тест всей системы D&D приложения
"""
import requests
import time
import random

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Красивый вывод секции"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_api():
    """Тестирование REST API"""
    
    print_section("🧪 БЫСТРЫЙ ТЕСТ D&D API")
    
    # Генерация случайного пользователя
    random_num = random.randint(1000, 9999)
    username = f"test_user_{random_num}"
    email = f"test_{random_num}@example.com"
    password = "TestPass123"
    
    print(f"\n📝 Тестовый пользователь:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    
    # Тест 1: Проверка здоровья
    print_section("1️⃣ Проверка здоровья сервера")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Сервер работает!")
            print(f"   Ответ: {response.json()}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Не удалось подключиться к серверу: {e}")
        print(f"   Убедитесь, что сервер запущен: python main.py")
        return
    
    # Тест 2: Регистрация
    print_section("2️⃣ Регистрация нового пользователя")
    try:
        response = requests.post(f"{BASE_URL}/api/users/register", json={
            "username": username,
            "email": email,
            "password": password,
            "confirm_password": password,
            "character_name": "Тестовый Герой"
        }, timeout=5)
        
        if response.status_code == 201:
            data = response.json()
            token = data['access_token']
            user = data['user']
            
            print("✅ Регистрация успешна!")
            print(f"   ID: {user['id']}")
            print(f"   Username: {user['username']}")
            print(f"   Email: {user['email']}")
            print(f"   Character: {user['character_name']}")
            print(f"   Token: {token[:50]}...")
        else:
            print(f"❌ Ошибка регистрации: {response.status_code}")
            print(f"   {response.json()}")
            return
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return
    
    time.sleep(1)
    
    # Тест 3: Вход
    print_section("3️⃣ Вход в систему")
    try:
        response = requests.post(f"{BASE_URL}/api/users/login", json={
            "username": username,
            "password": password
        }, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            
            print("✅ Вход успешен!")
            print(f"   Token: {token[:50]}...")
        else:
            print(f"❌ Ошибка входа: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return
    
    time.sleep(1)
    
    # Тест 4: Получение информации о текущем пользователе
    print_section("4️⃣ Получение информации о пользователе")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/users/me", headers=headers, timeout=5)
        
        if response.status_code == 200:
            user = response.json()
            print("✅ Информация получена!")
            print(f"   ID: {user['id']}")
            print(f"   Username: {user['username']}")
            print(f"   Email: {user['email']}")
            print(f"   Character: {user['character_name']}")
            print(f"   Active: {user['is_active']}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    time.sleep(1)
    
    # Тест 5: Получение списка пользователей
    print_section("5️⃣ Получение списка пользователей")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/users/", headers=headers, timeout=5)
        
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Получено пользователей: {len(users)}")
            for idx, user in enumerate(users[:5], 1):  # Показываем первых 5
                print(f"   {idx}. {user['username']} - {user['character_name'] or 'без персонажа'}")
            if len(users) > 5:
                print(f"   ... и еще {len(users) - 5}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Итоги
    print_section("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
    print("\n📋 Следующие шаги:")
    print("   1. Откройте Swagger UI: http://localhost:8000/docs")
    print("   2. Откройте test_client.html для тестирования Socket.IO")
    print(f"   3. Используйте этот токен для Socket.IO:")
    print(f"      {token}")
    print("\n🎲 Приятной игры!")


if __name__ == "__main__":
    test_api()