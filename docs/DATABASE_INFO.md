# 🗄️ База данных D&D приложения

## Структура базы данных

### Таблица `users`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INTEGER | Уникальный идентификатор (Primary Key, автоинкремент) |
| `username` | VARCHAR(50) | Имя пользователя (уникальное, индексированное) |
| `email` | VARCHAR(100) | Email пользователя (уникальный, индексированный) |
| `hashed_password` | VARCHAR(255) | Хешированный пароль |
| `character_name` | VARCHAR(100) | Имя персонажа (опционально) |
| `is_active` | BOOLEAN | Статус активности пользователя |
| `created_at` | DATETIME | Дата и время создания |
| `updated_at` | DATETIME | Дата и время последнего обновления |

## Файлы базы данных

### `bd.py`
Основной файл конфигурации базы данных:
- Настройка подключения к SQLite
- Модель `User`
- Функции инициализации БД

### `crud.py`
CRUD операции (Create, Read, Update, Delete):
- `create_user()` - создание нового пользователя
- `get_user_by_username()` - получение пользователя по имени
- `get_user_by_email()` - получение пользователя по email
- `get_user_by_id()` - получение пользователя по ID
- `authenticate_user()` - аутентификация пользователя
- `update_user()` - обновление данных пользователя
- `delete_user()` - удаление пользователя
- `get_all_users()` - получение списка всех пользователей

## Использование

### Инициализация базы данных

```python
from bd import init_db

# Создать все таблицы
init_db()
```

### Создание пользователя

```python
from bd import SessionLocal
from crud import create_user

db = SessionLocal()
try:
    user = create_user(
        db=db,
        username="dungeon_master",
        email="dm@example.com",
        password="SecurePass123",
        character_name="Арагорн"
    )
    print(f"Создан пользователь: {user.username}")
finally:
    db.close()
```

### Аутентификация пользователя

```python
from bd import SessionLocal
from crud import authenticate_user

db = SessionLocal()
try:
    user = authenticate_user(
        db=db,
        username="dungeon_master",
        password="SecurePass123"
    )
    if user:
        print(f"Успешная аутентификация: {user.username}")
    else:
        print("Неверные учетные данные")
finally:
    db.close()
```

## Безопасность

- Пароли хешируются с использованием **bcrypt**
- Используется библиотека **passlib** для работы с паролями
- Пароли никогда не хранятся в открытом виде

## База данных

- **Тип**: SQLite
- **Файл**: `dnd_app.db` (создается автоматически в корне проекта)
- **Кодировка**: UTF-8

## Примечания

- База данных автоматически создается при первом запуске
- Все индексы создаются автоматически для оптимизации запросов
- Поддержка временных меток (created_at, updated_at)