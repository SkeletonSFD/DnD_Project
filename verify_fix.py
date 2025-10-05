"""
Проверка исправления проблемы с токеном
"""
import sys
import os

# Добавляем путь к backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import timedelta
from app.auth import create_access_token, decode_access_token

def test_token_fix():
    """Тест исправления токена"""
    print("=" * 70)
    print("ПРОВЕРКА ИСПРАВЛЕНИЯ ТОКЕНА")
    print("=" * 70)
    
    # Тест 1: Создание токена со строковым ID
    print("\n1️⃣ ТЕСТ: Создание токена со строковым user_id")
    user_id = 4
    
    try:
        token = create_access_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(days=1)
        )
        print(f"   ✅ Токен создан успешно!")
        print(f"   Token: {token[:50]}...")
    except Exception as e:
        print(f"   ❌ Ошибка создания токена: {e}")
        return False
    
    # Тест 2: Декодирование токена
    print("\n2️⃣ ТЕСТ: Декодирование токена")
    try:
        payload = decode_access_token(token)
        if payload is None:
            print(f"   ❌ Токен не декодируется!")
            return False
        
        print(f"   ✅ Токен декодирован успешно!")
        print(f"   Payload: {payload}")
        
        # Проверяем, что sub - строка
        sub = payload.get("sub")
        print(f"   Sub value: {sub}")
        print(f"   Sub type: {type(sub).__name__}")
        
        if not isinstance(sub, str):
            print(f"   ⚠️  ВНИМАНИЕ: sub должен быть строкой, но это {type(sub).__name__}")
        else:
            print(f"   ✅ Sub является строкой!")
        
        # Проверяем, что можно преобразовать в int
        try:
            user_id_int = int(sub)
            print(f"   ✅ Sub можно преобразовать в int: {user_id_int}")
        except (ValueError, TypeError) as e:
            print(f"   ❌ Ошибка преобразования sub в int: {e}")
            return False
        
    except Exception as e:
        print(f"   ❌ Ошибка декодирования: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Тест 3: Проверка с разными ID
    print("\n3️⃣ ТЕСТ: Проверка с разными user_id")
    test_ids = [1, 4, 5, 100, 999]
    
    for test_id in test_ids:
        try:
            token = create_access_token(
                data={"sub": str(test_id)},
                expires_delta=timedelta(days=1)
            )
            payload = decode_access_token(token)
            sub = payload.get("sub")
            recovered_id = int(sub)
            
            if recovered_id == test_id:
                print(f"   ✅ ID {test_id}: OK")
            else:
                print(f"   ❌ ID {test_id}: Ожидалось {test_id}, получено {recovered_id}")
                return False
        except Exception as e:
            print(f"   ❌ ID {test_id}: Ошибка - {e}")
            return False
    
    print("\n" + "=" * 70)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    print("=" * 70)
    print("\n📝 ВЫВОД:")
    print("   Исправление работает корректно!")
    print("   Токены создаются и декодируются правильно.")
    print("   Теперь нужно перезапустить сервер, чтобы изменения вступили в силу.")
    print("\n🔄 СЛЕДУЮЩИЙ ШАГ:")
    print("   1. Остановите сервер (Ctrl+C)")
    print("   2. Запустите заново: python run.py")
    print("   3. Попробуйте войти на сайте")
    
    return True


if __name__ == "__main__":
    success = test_token_fix()
    sys.exit(0 if success else 1)