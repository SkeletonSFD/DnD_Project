"""
Socket.IO сервер для real-time коммуникации в D&D приложении
"""
import socketio
from typing import Dict, Set
from app.auth import decode_access_token
from app.bd import SessionLocal
from app.crud import get_user_by_id

# Создание Socket.IO сервера
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',  # В продакшене указать конкретные домены
    logger=True,
    engineio_logger=True
)

# Хранилище активных пользователей и комнат
active_users: Dict[str, dict] = {}  # sid -> user_info
game_rooms: Dict[str, Set[str]] = {}  # room_id -> set of sids


async def authenticate_socket(token: str) -> dict:
    """
    Аутентификация пользователя по токену для Socket.IO
    
    Args:
        token: JWT токен
    
    Returns:
        dict: Информация о пользователе или None
    """
    payload = decode_access_token(token)
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    db = SessionLocal()
    try:
        user = get_user_by_id(db, user_id)
        if user and user.is_active:
            return {
                "id": user.id,
                "username": user.username,
                "character_name": user.character_name
            }
    finally:
        db.close()
    
    return None


@sio.event
async def connect(sid, environ, auth):
    """
    Обработка подключения клиента
    """
    print(f"🔌 Клиент подключается: {sid}")
    
    # Проверка токена
    if not auth or 'token' not in auth:
        print(f"❌ Отклонено подключение {sid}: нет токена")
        return False
    
    user_info = await authenticate_socket(auth['token'])
    if not user_info:
        print(f"❌ Отклонено подключение {sid}: невалидный токен")
        return False
    
    # Сохранение информации о пользователе
    active_users[sid] = user_info
    
    print(f"✅ Пользователь подключен: {user_info['username']} (sid: {sid})")
    
    # Отправка приветственного сообщения
    await sio.emit('connected', {
        'message': f"Добро пожаловать, {user_info['username']}!",
        'user': user_info
    }, to=sid)
    
    # Уведомление всех о новом пользователе
    await sio.emit('user_joined', {
        'username': user_info['username'],
        'character_name': user_info['character_name']
    }, skip_sid=sid)
    
    return True


@sio.event
async def disconnect(sid):
    """
    Обработка отключения клиента
    """
    if sid in active_users:
        user_info = active_users[sid]
        print(f"🔌 Пользователь отключился: {user_info['username']} (sid: {sid})")
        
        # Удаление из всех комнат
        for room_id, members in game_rooms.items():
            if sid in members:
                members.remove(sid)
                await sio.emit('user_left_room', {
                    'username': user_info['username'],
                    'room_id': room_id
                }, room=room_id)
        
        # Уведомление всех об отключении
        await sio.emit('user_left', {
            'username': user_info['username']
        })
        
        del active_users[sid]
    else:
        print(f"🔌 Клиент отключился: {sid}")


@sio.event
async def join_room(sid, data):
    """
    Присоединение к игровой комнате
    """
    if sid not in active_users:
        return {'error': 'Не авторизован'}
    
    room_id = data.get('room_id')
    if not room_id:
        return {'error': 'Не указан ID комнаты'}
    
    user_info = active_users[sid]
    
    # Добавление в комнату
    if room_id not in game_rooms:
        game_rooms[room_id] = set()
    
    game_rooms[room_id].add(sid)
    sio.enter_room(sid, room_id)
    
    print(f"🚪 {user_info['username']} присоединился к комнате {room_id}")
    
    # Уведомление участников комнаты
    await sio.emit('user_joined_room', {
        'username': user_info['username'],
        'character_name': user_info['character_name'],
        'room_id': room_id
    }, room=room_id, skip_sid=sid)
    
    return {
        'success': True,
        'room_id': room_id,
        'members_count': len(game_rooms[room_id])
    }


@sio.event
async def leave_room(sid, data):
    """
    Выход из игровой комнаты
    """
    if sid not in active_users:
        return {'error': 'Не авторизован'}
    
    room_id = data.get('room_id')
    if not room_id:
        return {'error': 'Не указан ID комнаты'}
    
    user_info = active_users[sid]
    
    # Удаление из комнаты
    if room_id in game_rooms and sid in game_rooms[room_id]:
        game_rooms[room_id].remove(sid)
        sio.leave_room(sid, room_id)
        
        print(f"🚪 {user_info['username']} покинул комнату {room_id}")
        
        # Уведомление участников комнаты
        await sio.emit('user_left_room', {
            'username': user_info['username'],
            'room_id': room_id
        }, room=room_id)
        
        # Удаление пустой комнаты
        if len(game_rooms[room_id]) == 0:
            del game_rooms[room_id]
        
        return {'success': True}
    
    return {'error': 'Вы не в этой комнате'}


@sio.event
async def send_message(sid, data):
    """
    Отправка сообщения в чат
    """
    if sid not in active_users:
        return {'error': 'Не авторизован'}
    
    user_info = active_users[sid]
    room_id = data.get('room_id')
    message = data.get('message', '').strip()
    
    if not message:
        return {'error': 'Пустое сообщение'}
    
    message_data = {
        'username': user_info['username'],
        'character_name': user_info['character_name'],
        'message': message,
        'timestamp': data.get('timestamp')
    }
    
    if room_id:
        # Отправка в комнату
        await sio.emit('chat_message', message_data, room=room_id)
        print(f"💬 [{room_id}] {user_info['username']}: {message}")
    else:
        # Отправка всем
        await sio.emit('chat_message', message_data)
        print(f"💬 [Общий чат] {user_info['username']}: {message}")
    
    return {'success': True}


@sio.event
async def dice_roll(sid, data):
    """
    Бросок кубика
    """
    if sid not in active_users:
        return {'error': 'Не авторизован'}
    
    user_info = active_users[sid]
    room_id = data.get('room_id')
    dice_type = data.get('dice_type', 'd20')  # d4, d6, d8, d10, d12, d20, d100
    result = data.get('result')
    
    roll_data = {
        'username': user_info['username'],
        'character_name': user_info['character_name'],
        'dice_type': dice_type,
        'result': result,
        'timestamp': data.get('timestamp')
    }
    
    if room_id:
        await sio.emit('dice_rolled', roll_data, room=room_id)
        print(f"🎲 [{room_id}] {user_info['username']} бросил {dice_type}: {result}")
    else:
        await sio.emit('dice_rolled', roll_data)
        print(f"🎲 {user_info['username']} бросил {dice_type}: {result}")
    
    return {'success': True}


@sio.event
async def get_online_users(sid, data):
    """
    Получение списка онлайн пользователей
    """
    if sid not in active_users:
        return {'error': 'Не авторизован'}
    
    room_id = data.get('room_id')
    
    if room_id and room_id in game_rooms:
        # Пользователи в конкретной комнате
        users = [
            active_users[user_sid]
            for user_sid in game_rooms[room_id]
            if user_sid in active_users
        ]
    else:
        # Все онлайн пользователи
        users = list(active_users.values())
    
    return {
        'users': users,
        'count': len(users)
    }


# Экспорт Socket.IO приложения
socketio_app = socketio.ASGIApp(
    sio,
    socketio_path='socket.io'
)