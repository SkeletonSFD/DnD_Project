"""
Полный тест flow логина: login -> получение токена -> получение данных пользователя
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_full_login_flow():
    """Полный тест логина и получения данных пользователя"""
    print("=" * 70)
    print("ПОЛНЫЙ ТЕСТ ЛОГИНА")
    print("=" * 70)
    
    username = "SFDSkeleton"
    password = "Irina25011965"
    
    print(f"\n1️⃣ ШАГ 1: ЛОГИН")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    
    # Шаг 1: Логин
    form_data = {
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/users/login",
            data=form_data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ ОШИБКА ЛОГИНА!")
            print(f"   Response: {response.text}")
            return False
        
        login_data = response.json()
        access_token = login_data['access_token']
        
        print(f"   ✅ ЛОГИН УСПЕШЕН!")
        print(f"   Token: {access_token[:50]}...")
        print(f"   User ID: {login_data['user']['id']}")
        print(f"   Username: {login_data['user']['username']}")
        
        # Шаг 2: Получение данных пользователя
        print(f"\n2️⃣ ШАГ 2: ПОЛУЧЕНИЕ ДАННЫХ ПОЛЬЗОВАТЕЛЯ")
        print(f"   Endpoint: /api/users/me")
        print(f"   Authorization: Bearer {access_token[:30]}...")
        
        response2 = requests.get(
            f"{BASE_URL}/api/users/me",
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        
        print(f"   Status Code: {response2.status_code}")
        
        if response2.status_code != 200:
            print(f"   ❌ ОШИБКА ПОЛУЧЕНИЯ ДАННЫХ!")
            print(f"   Response: {response2.text}")
            
            # Попробуем декодировать токен
            print(f"\n🔍 ОТЛАДКА ТОКЕНА:")
            import base64
            try:
                # JWT состоит из 3 частей: header.payload.signature
                parts = access_token.split('.')
                if len(parts) == 3:
                    # Декодируем payload (вторая часть)
                    payload = parts[1]
                    # Добавляем padding если нужно
                    padding = 4 - len(payload) % 4
                    if padding != 4:
                        payload += '=' * padding
                    
                    decoded = base64.urlsafe_b64decode(payload)
                    print(f"   Payload: {decoded.decode('utf-8')}")
            except Exception as e:
                print(f"   Ошибка декодирования: {e}")
            
            return False
        
        user_data = response2.json()
        
        print(f"   ✅ ДАННЫЕ ПОЛУЧЕНЫ!")
        print(f"   User ID: {user_data['id']}")
        print(f"   Username: {user_data['username']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Character Name: {user_data.get('character_name', 'None')}")
        
        print(f"\n{'=' * 70}")
        print(f"✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print(f"{'=' * 70}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ОШИБКА: Не удалось подключиться к серверу")
        print(f"Убедитесь, что сервер запущен на {BASE_URL}")
        return False
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_full_login_flow()