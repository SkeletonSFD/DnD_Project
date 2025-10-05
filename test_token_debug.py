"""
Детальная отладка проблемы с токеном
"""
import requests
import json
from jose import jwt, JWTError

BASE_URL = "http://localhost:8000"
SECRET_KEY = "your-secret-key-here-change-in-production-123456789"
ALGORITHM = "HS256"

def test_token():
    """Тест токена"""
    print("=" * 70)
    print("ОТЛАДКА ТОКЕНА")
    print("=" * 70)
    
    # Шаг 1: Получаем токен
    print("\n1️⃣ ПОЛУЧЕНИЕ ТОКЕНА")
    form_data = {
        'username': 'SFDSkeleton',
        'password': 'Irina25011965'
    }
    
    response = requests.post(
        f"{BASE_URL}/api/users/login",
        data=form_data
    )
    
    if response.status_code != 200:
        print(f"❌ Ошибка логина: {response.text}")
        return
    
    login_data = response.json()
    token = login_data['access_token']
    
    print(f"✅ Токен получен: {token[:50]}...")
    
    # Шаг 2: Декодируем токен локально
    print(f"\n2️⃣ ДЕКОДИРОВАНИЕ ТОКЕНА ЛОКАЛЬНО")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ Токен валиден!")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        user_id = payload.get('sub')
        print(f"   User ID из токена: {user_id}")
    except JWTError as e:
        print(f"❌ Ошибка декодирования: {e}")
        return
    
    # Шаг 3: Проверяем разные варианты отправки токена
    print(f"\n3️⃣ ТЕСТИРОВАНИЕ РАЗНЫХ ВАРИАНТОВ ОТПРАВКИ ТОКЕНА")
    
    variants = [
        {
            'name': 'Вариант 1: Authorization: Bearer <token>',
            'headers': {
                'Authorization': f'Bearer {token}'
            }
        },
        {
            'name': 'Вариант 2: Authorization: Bearer <token> + Content-Type: application/json',
            'headers': {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        },
        {
            'name': 'Вариант 3: Только токен без Bearer',
            'headers': {
                'Authorization': token
            }
        }
    ]
    
    for variant in variants:
        print(f"\n   {variant['name']}")
        print(f"   Headers: {variant['headers']}")
        
        response = requests.get(
            f"{BASE_URL}/api/users/me",
            headers=variant['headers']
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ УСПЕХ!")
            user_data = response.json()
            print(f"   User: {user_data['username']}")
        else:
            print(f"   ❌ ОШИБКА: {response.text}")
    
    # Шаг 4: Проверяем, что сервер видит в заголовках
    print(f"\n4️⃣ ПРОВЕРКА HEALTH ENDPOINT")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Сервер работает")
        print(f"   Response: {response.json()}")


if __name__ == "__main__":
    test_token()