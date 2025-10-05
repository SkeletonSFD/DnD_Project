# 📚 D&D Application API Documentation

## 🚀 Запуск сервера

```bash
python main.py
```

Сервер запустится на `http://localhost:8000`

## 📖 Документация API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 REST API Endpoints

### 1. Регистрация пользователя

**POST** `/api/users/register`

**Body:**
```json
{
  "username": "dungeon_master",
  "email": "dm@example.com",
  "password": "SecurePass123",
  "confirm_password": "SecurePass123",
  "character_name": "Арагорн"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "dungeon_master",
    "email": "dm@example.com",
    "character_name": "Арагорн",
    "is_active": true
  }
}
```

### 2. Вход в систему

**POST** `/api/users/login`

**Body:**
```json
{
  "username": "dungeon_master",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "dungeon_master",
    "email": "dm@example.com",
    "character_name": "Арагорн",
    "is_active": true
  }
}
```

### 3. Получение информации о текущем пользователе

**GET** `/api/users/me`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "username": "dungeon_master",
  "email": "dm@example.com",
  "character_name": "Арагорн",
  "is_active": true
}
```

### 4. Получение списка пользователей

**GET** `/api/users/?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "id": 1,
    "username": "dungeon_master",
    "email": "dm@example.com",
    "character_name": "Арагорн",
    "is_active": true
  }
]
```

## 🔌 Socket.IO Events

### Подключение

```javascript
const socket = io('http://localhost:8000', {
  auth: { token: 'your_jwt_token' },
  transports: ['websocket']
});
```

### События от сервера

#### `connected`
Приветственное сообщение после подключения
```json
{
  "message": "Добро пожаловать, dungeon_master!",
  "user": {
    "id": 1,
    "username": "dungeon_master",
    "character_name": "Арагорн"
  }
}
```

#### `user_joined`
Новый пользователь присоединился
```json
{
  "username": "new_player",
  "character_name": "Гэндальф"
}
```

#### `user_left`
Пользователь вышел
```json
{
  "username": "player_name"
}
```

#### `user_joined_room`
Пользователь присоединился к комнате
```json
{
  "username": "player_name",
  "character_name": "Леголас",
  "room_id": "game_room_1"
}
```

#### `user_left_room`
Пользователь покинул комнату
```json
{
  "username": "player_name",
  "room_id": "game_room_1"
}
```

#### `chat_message`
Сообщение в чате
```json
{
  "username": "dungeon_master",
  "character_name": "Арагорн",
  "message": "Привет всем!",
  "timestamp": 1234567890
}
```

#### `dice_rolled`
Бросок кубика
```json
{
  "username": "dungeon_master",
  "character_name": "Арагорн",
  "dice_type": "d20",
  "result": 18,
  "timestamp": 1234567890
}
```

### События от клиента

#### `join_room`
Присоединиться к комнате
```javascript
socket.emit('join_room', { room_id: 'game_room_1' }, (response) => {
  console.log(response);
  // { success: true, room_id: 'game_room_1', members_count: 3 }
});
```

#### `leave_room`
Покинуть комнату
```javascript
socket.emit('leave_room', { room_id: 'game_room_1' }, (response) => {
  console.log(response);
  // { success: true }
});
```

#### `send_message`
Отправить сообщение
```javascript
socket.emit('send_message', {
  room_id: 'game_room_1',  // опционально, если не указано - отправка всем
  message: 'Привет!',
  timestamp: Date.now()
}, (response) => {
  console.log(response);
  // { success: true }
});
```

#### `dice_roll`
Бросить кубик
```javascript
socket.emit('dice_roll', {
  room_id: 'game_room_1',  // опционально
  dice_type: 'd20',
  result: 15,
  timestamp: Date.now()
}, (response) => {
  console.log(response);
  // { success: true }
});
```

#### `get_online_users`
Получить список онлайн пользователей
```javascript
socket.emit('get_online_users', {
  room_id: 'game_room_1'  // опционально, если не указано - все онлайн
}, (response) => {
  console.log(response);
  // { users: [...], count: 3 }
});
```

## 🎲 Типы кубиков

- `d4` - 4-гранный кубик (1-4)
- `d6` - 6-гранный кубик (1-6)
- `d8` - 8-гранный кубик (1-8)
- `d10` - 10-гранный кубик (1-10)
- `d12` - 12-гранный кубик (1-12)
- `d20` - 20-гранный кубик (1-20)
- `d100` - 100-гранный кубик (1-100)

## 🧪 Тестирование

### 1. Тестирование REST API

Используйте Swagger UI: http://localhost:8000/docs

### 2. Тестирование Socket.IO

#### Вариант 1: HTML клиент
Откройте `test_client.html` в браузере

#### Вариант 2: Python клиент
```bash
# Установите socketio клиент
pip install python-socketio[client]

# Запустите тест
python test_socketio_client.py
```

## 📝 Примеры использования

### Python (requests + socketio)

```python
import requests
import socketio

# 1. Регистрация
response = requests.post('http://localhost:8000/api/users/register', json={
    'username': 'test_user',
    'email': 'test@example.com',
    'password': 'TestPass123',
    'confirm_password': 'TestPass123',
    'character_name': 'Тестовый персонаж'
})

data = response.json()
token = data['access_token']

# 2. Подключение к Socket.IO
sio = socketio.Client()

@sio.on('connected')
def on_connected(data):
    print(f"Подключено: {data}")

sio.connect('http://localhost:8000', auth={'token': token})

# 3. Присоединение к комнате
sio.emit('join_room', {'room_id': 'test_room'})

# 4. Отправка сообщения
sio.emit('send_message', {
    'room_id': 'test_room',
    'message': 'Привет!',
    'timestamp': time.time()
})

# 5. Бросок кубика
sio.emit('dice_roll', {
    'room_id': 'test_room',
    'dice_type': 'd20',
    'result': 15,
    'timestamp': time.time()
})
```

### JavaScript (fetch + socket.io)

```javascript
// 1. Регистрация
const response = await fetch('http://localhost:8000/api/users/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'test_user',
    email: 'test@example.com',
    password: 'TestPass123',
    confirm_password: 'TestPass123',
    character_name: 'Тестовый персонаж'
  })
});

const data = await response.json();
const token = data.access_token;

// 2. Подключение к Socket.IO
const socket = io('http://localhost:8000', {
  auth: { token: token },
  transports: ['websocket']
});

socket.on('connected', (data) => {
  console.log('Подключено:', data);
});

// 3. Присоединение к комнате
socket.emit('join_room', { room_id: 'test_room' });

// 4. Отправка сообщения
socket.emit('send_message', {
  room_id: 'test_room',
  message: 'Привет!',
  timestamp: Date.now()
});

// 5. Бросок кубика
socket.emit('dice_roll', {
  room_id: 'test_room',
  dice_type: 'd20',
  result: Math.floor(Math.random() * 20) + 1,
  timestamp: Date.now()
});
```

## 🔒 Безопасность

- Пароли хешируются с помощью bcrypt
- JWT токены для аутентификации
- CORS настроен (в продакшене указать конкретные домены)
- Socket.IO требует валидный JWT токен для подключения

## ⚙️ Конфигурация

### Изменение SECRET_KEY

В файле `auth.py` измените:
```python
SECRET_KEY = "your-secret-key-here"  # Используйте переменную окружения
```

### Изменение времени жизни токена

В файле `auth.py`:
```python
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 часа
```

### Изменение порта

В файле `main.py`:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8000)
```