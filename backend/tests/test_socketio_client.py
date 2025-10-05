"""
Тестовый клиент для проверки Socket.IO соединения
"""
import socketio
import asyncio
import time

# URL сервера
SERVER_URL = "http://localhost:8000"

# Токен для аутентификации (нужно получить через /api/users/login)
# Замените на реальный токен после регистрации/входа
TOKEN = "your_jwt_token_here"


async def test_socketio():
    """Тестирование Socket.IO соединения"""
    
    # Создание клиента
    sio = socketio.AsyncClient(logger=True, engineio_logger=True)
    
    # Обработчики событий
    @sio.event
    async def connect():
        print("✅ Подключено к серверу!")
    
    @sio.event
    async def connected(data):
        print(f"📨 Получено приветствие: {data}")
    
    @sio.event
    async def disconnect():
        print("❌ Отключено от сервера")
    
    @sio.event
    async def user_joined(data):
        print(f"👤 Пользователь присоединился: {data}")
    
    @sio.event
    async def user_left(data):
        print(f"👤 Пользователь вышел: {data}")
    
    @sio.event
    async def chat_message(data):
        print(f"💬 Сообщение от {data['username']}: {data['message']}")
    
    @sio.event
    async def dice_rolled(data):
        print(f"🎲 {data['username']} бросил {data['dice_type']}: {data['result']}")
    
    @sio.event
    async def user_joined_room(data):
        print(f"🚪 {data['username']} присоединился к комнате {data['room_id']}")
    
    @sio.event
    async def user_left_room(data):
        print(f"🚪 {data['username']} покинул комнату {data['room_id']}")
    
    try:
        # Подключение к серверу с токеном
        print(f"🔌 Подключение к {SERVER_URL}...")
        await sio.connect(
            SERVER_URL,
            auth={'token': TOKEN},
            transports=['websocket']
        )
        
        # Ожидание подключения
        await asyncio.sleep(2)
        
        # Тест 1: Присоединение к комнате
        print("\n📍 Тест 1: Присоединение к комнате...")
        response = await sio.call('join_room', {'room_id': 'test_room_1'})
        print(f"Ответ: {response}")
        
        await asyncio.sleep(1)
        
        # Тест 2: Отправка сообщения в комнату
        print("\n📍 Тест 2: Отправка сообщения в комнату...")
        response = await sio.call('send_message', {
            'room_id': 'test_room_1',
            'message': 'Привет из тестового клиента!',
            'timestamp': time.time()
        })
        print(f"Ответ: {response}")
        
        await asyncio.sleep(1)
        
        # Тест 3: Бросок кубика
        print("\n📍 Тест 3: Бросок кубика...")
        import random
        dice_result = random.randint(1, 20)
        response = await sio.call('dice_roll', {
            'room_id': 'test_room_1',
            'dice_type': 'd20',
            'result': dice_result,
            'timestamp': time.time()
        })
        print(f"Ответ: {response}")
        
        await asyncio.sleep(1)
        
        # Тест 4: Получение списка онлайн пользователей
        print("\n📍 Тест 4: Получение списка онлайн пользователей...")
        response = await sio.call('get_online_users', {'room_id': 'test_room_1'})
        print(f"Ответ: {response}")
        
        await asyncio.sleep(1)
        
        # Тест 5: Выход из комнаты
        print("\n📍 Тест 5: Выход из комнаты...")
        response = await sio.call('leave_room', {'room_id': 'test_room_1'})
        print(f"Ответ: {response}")
        
        # Ожидание перед отключением
        await asyncio.sleep(2)
        
        # Отключение
        await sio.disconnect()
        print("\n✅ Все тесты завершены!")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 ТЕСТИРОВАНИЕ SOCKET.IO КЛИЕНТА")
    print("=" * 60)
    print("\n⚠️  ВАЖНО: Перед запуском теста:")
    print("1. Запустите сервер: python main.py")
    print("2. Зарегистрируйтесь или войдите через API")
    print("3. Скопируйте полученный токен в переменную TOKEN")
    print("4. Запустите этот скрипт\n")
    
    if TOKEN == "your_jwt_token_here":
        print("❌ ОШИБКА: Укажите реальный JWT токен в переменной TOKEN!")
        print("   Получите токен через POST /api/users/login или /api/users/register")
    else:
        asyncio.run(test_socketio())