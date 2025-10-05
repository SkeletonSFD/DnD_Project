# 📁 Структура проекта D&D Application

## 🗂️ Обзор структуры

Проект организован в модульную структуру с разделением на backend, frontend и документацию.

```
DnD_Project/
│
├── 📂 backend/                          # Backend приложение
│   ├── 📂 app/                         # Основной код приложения
│   │   ├── __init__.py                # Инициализация пакета (версия 1.0.0)
│   │   ├── main.py                    # Точка входа FastAPI приложения
│   │   ├── auth.py                    # JWT аутентификация и авторизация
│   │   ├── bd.py                      # Модели базы данных SQLAlchemy
│   │   ├── crud.py                    # CRUD операции для БД
│   │   ├── routes_users.py            # API роуты для пользователей
│   │   ├── schemas.py                 # Pydantic схемы валидации
│   │   └── socketio_server.py         # Socket.IO сервер для real-time
│   │
│   ├── 📂 tests/                       # Тестирование
│   │   ├── __init__.py                # Инициализация тестового пакета
│   │   ├── quick_test.py              # Быстрый тест всех API endpoints
│   │   ├── test_db.py                 # Тестирование базы данных
│   │   └── test_socketio_client.py    # Тестирование Socket.IO клиента
│   │
│   ├── requirements.txt                # Python зависимости
│   └── dnd_app.db                     # SQLite база данных
│
├── 📂 frontend/                         # Frontend файлы
│   └── test_client.html               # HTML тестовый клиент с Socket.IO
│
├── 📂 docs/                            # Документация проекта
│   ├── README.md                      # Основная документация (детальная)
│   ├── QUICKSTART.md                  # Быстрый старт (7.4 KB)
│   ├── API_DOCUMENTATION.md           # Полная документация API (9.3 KB)
│   ├── DATABASE_INFO.md               # Информация о структуре БД (3.9 KB)
│   ├── FEATURES.md                    # Описание всех функций (15.5 KB)
│   ├── PROJECT_STATUS.md              # Текущий статус проекта (12.2 KB)
│   ├── PROJECT_SUMMARY.md             # Краткое описание проекта (9.9 KB)
│   ├── SETUP_SUMMARY.md               # Инструкции по установке (4.7 KB)
│   ├── FINAL_SUMMARY.md               # Финальное резюме (17.7 KB)
│   ├── CHECKLIST.md                   # Полный чеклист проекта (12.8 KB)
│   └── PROJECT_FILES.md               # Описание всех файлов (15.5 KB)
│
├── README.md                           # Главный README проекта
├── run.py                             # Скрипт запуска из корня проекта
├── .gitignore                         # Git ignore правила
└── DnD_Project.iml                    # IntelliJ IDEA конфигурация

```

## 📊 Статистика файлов

### По категориям

| Категория | Файлов | Размер | Описание |
|-----------|--------|--------|----------|
| **Backend Code** | 8 | ~35 KB | Python код приложения |
| **Tests** | 4 | ~16 KB | Тестовые файлы |
| **Frontend** | 1 | ~17 KB | HTML клиент |
| **Documentation** | 11 | ~110 KB | Markdown документация |
| **Config** | 3 | ~9 KB | Конфигурационные файлы |
| **Database** | 1 | ~20 KB | SQLite база данных |
| **TOTAL** | **28** | **~207 KB** | Весь проект |

### Backend файлы (app/)

| Файл | Размер | Строк | Описание |
|------|--------|-------|----------|
| `main.py` | 2.6 KB | ~86 | FastAPI приложение, CORS, роуты |
| `auth.py` | 3.9 KB | ~129 | JWT токены, аутентификация |
| `bd.py` | 2.8 KB | ~74 | SQLAlchemy модели, User |
| `crud.py` | 5.7 KB | ~184 | CRUD операции для пользователей |
| `routes_users.py` | 6.5 KB | ~189 | 4 API endpoint'а |
| `schemas.py` | 4.3 KB | ~142 | Pydantic схемы валидации |
| `socketio_server.py` | 9.0 KB | ~280 | 8 Socket.IO событий |
| `__init__.py` | 0.1 KB | ~6 | Инициализация пакета |

### Тестовые файлы (tests/)

| Файл | Размер | Описание |
|------|--------|----------|
| `quick_test.py` | 5.9 KB | Быстрый тест API (регистрация, логин, список) |
| `test_db.py` | 4.2 KB | Тест базы данных (CRUD операции) |
| `test_socketio_client.py` | 5.5 KB | Тест Socket.IO (чат, кубики, комнаты) |
| `__init__.py` | 0.04 KB | Инициализация тестового пакета |

### Документация (docs/)

| Файл | Размер | Описание |
|------|--------|----------|
| `README.md` | 11.7 KB | Основная документация |
| `QUICKSTART.md` | 7.4 KB | Быстрый старт |
| `API_DOCUMENTATION.md` | 9.3 KB | Документация API |
| `FEATURES.md` | 15.5 KB | Все функции с примерами |
| `FINAL_SUMMARY.md` | 17.7 KB | Финальное резюме |
| `PROJECT_FILES.md` | 15.5 KB | Описание файлов |
| `PROJECT_STATUS.md` | 12.2 KB | Статус проекта |
| `CHECKLIST.md` | 12.8 KB | Чеклист (100% готово) |
| `PROJECT_SUMMARY.md` | 9.9 KB | Краткое описание |
| `DATABASE_INFO.md` | 3.9 KB | Информация о БД |
| `SETUP_SUMMARY.md` | 4.7 KB | Инструкции установки |

## 🔗 Зависимости между модулями

```
main.py
  ├── routes_users.py
  │     ├── bd.py (get_db, User)
  │     ├── crud.py (create_user, authenticate_user, etc.)
  │     ├── schemas.py (UserRegistrationRequest, etc.)
  │     └── auth.py (create_access_token, get_current_active_user)
  │
  ├── socketio_server.py
  │     ├── auth.py (decode_access_token)
  │     ├── bd.py (SessionLocal)
  │     └── crud.py (get_user_by_id)
  │
  └── bd.py (init_db)

auth.py
  ├── bd.py (get_db, User)
  └── crud.py (get_user_by_id)

crud.py
  └── bd.py (User)

routes_users.py
  ├── bd.py
  ├── crud.py
  ├── schemas.py
  └── auth.py
```

## 🚀 Точки входа

### 1. Запуск из корня проекта
```bash
python run.py
```
- Использует `run.py` в корне
- Автоматически добавляет backend в PYTHONPATH
- Запускает uvicorn с reload

### 2. Запуск из backend/app
```bash
cd backend/app
python main.py
```
- Прямой запуск main.py
- Требует правильных импортов (app.*)

### 3. Запуск через uvicorn
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Профессиональный способ
- Полный контроль над параметрами

## 📦 Импорты

### Абсолютные импорты (используются в проекте)

Все модули используют абсолютные импорты от пакета `app`:

```python
# В main.py
from app.routes_users import router as users_router
from app.socketio_server import socketio_app, sio
from app.bd import init_db

# В routes_users.py
from app.bd import get_db, User
from app.crud import create_user, authenticate_user
from app.schemas import UserRegistrationRequest
from app.auth import create_access_token

# В auth.py
from app.bd import get_db, User
from app.crud import get_user_by_id

# И т.д.
```

### Почему абсолютные импорты?

✅ **Преимущества:**
- Явные и понятные зависимости
- Работают из любой директории
- Совместимы с uvicorn
- Легко рефакторить

❌ **Относительные импорты** (не используются):
```python
from .bd import User  # Не используем
from ..app.crud import create_user  # Не используем
```

## 🗄️ База данных

### Расположение
```
backend/dnd_app.db
```

### Путь в коде
```python
# backend/app/bd.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'dnd_app.db')}"
```

Это создает путь: `backend/dnd_app.db`

### Структура таблиц

**users**
- id (Integer, PK)
- username (String, unique)
- email (String, unique)
- hashed_password (String)
- character_name (String, nullable)
- is_active (Boolean)
- created_at (DateTime)
- updated_at (DateTime)

## 🧪 Тестирование

### Запуск тестов

```bash
# Из корня проекта
cd backend/tests

# Быстрый тест API
python quick_test.py

# Тест базы данных
python test_db.py

# Тест Socket.IO
python test_socketio_client.py
```

### HTML клиент

```bash
# Открыть в браузере
frontend/test_client.html
```

## 📚 Документация

Вся документация находится в папке `docs/`:

### Для начинающих
1. **README.md** - Начните здесь
2. **QUICKSTART.md** - Быстрый старт
3. **FEATURES.md** - Что умеет приложение

### Для разработчиков
1. **API_DOCUMENTATION.md** - Полная документация API
2. **DATABASE_INFO.md** - Структура БД
3. **PROJECT_FILES.md** - Описание файлов

### Для менеджеров
1. **PROJECT_STATUS.md** - Текущий статус
2. **CHECKLIST.md** - Что готово (100%)
3. **FINAL_SUMMARY.md** - Полное резюме

## 🔧 Конфигурация

### requirements.txt
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-socketio==5.10.0
python-jose[cryptography]==3.3.0
bcrypt==4.1.1
sqlalchemy==2.0.23
pydantic[email]==2.5.0
```

### .gitignore
Исключает:
- `__pycache__/`
- `.venv/`
- `*.db`
- `.idea/`
- `.vscode/`
- `*.log`

## 🎯 Следующие шаги

### Phase 2 (Планируется)
- Управление персонажами (D&D характеристики)
- Система инвентаря
- Управление заклинаниями
- Боевая система

### Рекомендации
1. Создать `backend/.env` для секретных ключей
2. Добавить миграции (Alembic)
3. Добавить unit тесты (pytest)
4. Создать Docker контейнер
5. Настроить CI/CD

## 📝 Примечания

- Проект использует **Python 3.11+**
- База данных **SQLite** (для production рекомендуется PostgreSQL)
- **SECRET_KEY** в `auth.py` нужно изменить для production
- CORS настроен на `*` (для production указать конкретные домены)

---

**Последнее обновление**: 2025  
**Версия**: 1.0.0  
**Статус**: ✅ Готово к использованию