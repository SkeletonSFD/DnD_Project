"""
Тестирование входа с паролем Irina25011965
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_login(username, password):
    """Тест логина через API"""
    print(f"\n{'='*60}")
    print(f"ТЕСТ ЛОГИНА")
    print(f"{'='*60}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    
    # Формируем данные как form-data (OAuth2 стандарт)
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
        
        print(f"\nStatus Code: {response.status_code}")
        
        response_data = response.json()
        
        if response.status_code == 200:
            print(f"\n✅ ЛОГИН УСПЕШЕН!")
            print(f"\nДанные пользователя:")
            print(f"  User ID: {response_data['user']['id']}")
            print(f"  Username: {response_data['user']['username']}")
            print(f"  Email: {response_data['user']['email']}")
            print(f"  Character Name: {response_data['user'].get('character_name', 'None')}")
            print(f"\nТокен доступа:")
            print(f"  {response_data['access_token'][:50]}...")
            return True
        else:
            print(f"\n❌ ЛОГИН ПРОВАЛИЛСЯ!")
            print(f"Ошибка: {response_data.get('detail', 'Unknown error')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ОШИБКА: Не удалось подключиться к серверу")
        print(f"Убедитесь, что сервер запущен на {BASE_URL}")
        return False
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        return False


if __name__ == "__main__":
    print("="*60)
    print("ТЕСТИРОВАНИЕ ВХОДА С ПАРОЛЕМ Irina25011965")
    print("="*60)
    
    # Тест с паролем Irina25011965
    success = test_login("SFDSkeleton", "Irina25011965")
    
    if success:
        print("\n" + "="*60)
        print("✅ ВСЕ РАБОТАЕТ!")
        print("="*60)
        print("\nТеперь вы можете войти на сайте:")
        print("  1. Откройте: http://localhost:8000/static/index.html")
        print("  2. Введите:")
        print("     Имя персонажа: SFDSkeleton")
        print("     Секретная фраза: Irina25011965")
        print("  3. Нажмите 'Войти в королевство'")
    else:
        print("\n" + "="*60)
        print("❌ ЧТО-ТО ПОШЛО НЕ ТАК")
        print("="*60)
        print("\nПроверьте, что сервер запущен:")
        print("  python run.py")