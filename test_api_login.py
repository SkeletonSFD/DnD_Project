"""
Тестирование API логина напрямую
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_login(username, password):
    """Тест логина через API"""
    print(f"\n{'='*60}")
    print(f"ТЕСТ ЛОГИНА ЧЕРЕЗ API")
    print(f"{'='*60}")
    print(f"URL: {BASE_URL}/api/users/login")
    print(f"Username: {username}")
    print(f"Password: {password}")
    
    # Формируем данные как form-data (OAuth2 стандарт)
    form_data = {
        'username': username,
        'password': password
    }
    
    print(f"\nОтправляемые данные (form-data):")
    print(json.dumps(form_data, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/users/login",
            data=form_data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        
        print(f"\n{'='*60}")
        print(f"ОТВЕТ СЕРВЕРА")
        print(f"{'='*60}")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"\nТело ответа:")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            
            if response.status_code == 200:
                print(f"\n✅ ЛОГИН УСПЕШЕН!")
                print(f"Access Token: {response_data.get('access_token', 'N/A')[:50]}...")
                print(f"Token Type: {response_data.get('token_type', 'N/A')}")
                if 'user' in response_data:
                    print(f"User ID: {response_data['user'].get('id', 'N/A')}")
                    print(f"Username: {response_data['user'].get('username', 'N/A')}")
                return True
            else:
                print(f"\n❌ ЛОГИН ПРОВАЛИЛСЯ!")
                print(f"Ошибка: {response_data.get('detail', 'Unknown error')}")
                return False
                
        except json.JSONDecodeError:
            print(f"\nТело ответа (текст):")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ОШИБКА: Не удалось подключиться к серверу")
        print(f"Убедитесь, что сервер запущен на {BASE_URL}")
        return False
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        return False


def test_login_json(username, password):
    """Тест логина через API с JSON (для сравнения)"""
    print(f"\n{'='*60}")
    print(f"ТЕСТ ЛОГИНА ЧЕРЕЗ API (JSON)")
    print(f"{'='*60}")
    print(f"URL: {BASE_URL}/api/users/login")
    print(f"Username: {username}")
    print(f"Password: {password}")
    
    # Формируем данные как JSON
    json_data = {
        'username': username,
        'password': password
    }
    
    print(f"\nОтправляемые данные (JSON):")
    print(json.dumps(json_data, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/users/login",
            json=json_data
        )
        
        print(f"\n{'='*60}")
        print(f"ОТВЕТ СЕРВЕРА")
        print(f"{'='*60}")
        print(f"Status Code: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"\nТело ответа:")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            
            if response.status_code == 200:
                print(f"\n✅ ЛОГИН УСПЕШЕН!")
                return True
            else:
                print(f"\n❌ ЛОГИН ПРОВАЛИЛСЯ!")
                print(f"Ошибка: {response_data.get('detail', 'Unknown error')}")
                return False
                
        except json.JSONDecodeError:
            print(f"\nТело ответа (текст):")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ОШИБКА: Не удалось подключиться к серверу")
        return False
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        return False


if __name__ == "__main__":
    print("="*60)
    print("ТЕСТИРОВАНИЕ API ЛОГИНА")
    print("="*60)
    print("\nУбедитесь, что сервер запущен на http://localhost:8000")
    print("Запустите: python run.py")
    
    input("\nНажмите Enter для продолжения...")
    
    # Тест 1: Form-data (правильный способ для OAuth2)
    test_login("SFDSkeleton", "Password123")
    
    # Тест 2: JSON (неправильный способ, но для сравнения)
    test_login_json("SFDSkeleton", "Password123")
    
    # Тест 3: TestUser123
    test_login("TestUser123", "Password123")
    
    # Тест 4: Неверный пароль
    print("\n" + "="*60)
    print("ТЕСТ С НЕВЕРНЫМ ПАРОЛЕМ")
    print("="*60)
    test_login("SFDSkeleton", "WrongPassword123")