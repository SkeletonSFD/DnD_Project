# 🔄 Руководство по новой структуре проекта

## ✅ Что изменилось?

Проект был реорганизован в профессиональную модульную структуру:

### Старая структура (плоская)
```
DnD_Project/
├── main.py
├── auth.py
├── bd.py
├── crud.py
├── routes_users.py
├── schemas.py
├── socketio_server.py
├── test_db.py
├── quick_test.py
├── test_socketio_client.py
├── test_client.html
├── requirements.txt
├── dnd_app.db
├── README.md
├── API_DOCUMENTATION.md
└── ... (другие .md файлы)
```

### Новая структура (модульная)
```
DnD_Project/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── bd.py
│   │   ├── crud.py
│   │   ├── routes_users.py
│   │   ├── schemas.py
│   │   └── socketio_server.py
│   ├── tests/
│   │   ├── test_db.py
│   │   ├── quick_test.py
│   │   └── test_socketio_client.py
│   ├── requirements.txt
│   └── dnd_app.db
├── frontend/
│   └── test_client.html
├── docs/
│   ├── README.md
│   ├── API_DOCUMENTATION.md
│   └── ... (все .md файлы)
├── README.md
└── run.py
```

## 🎯 Преимущества новой структуры

### 1. **Модульность**
- ✅ Четкое разделение backend/frontend/docs
- ✅ Легко масштабировать
- ✅ Проще навигация

### 2. **Профессиональность**
- ✅ Соответствует стандартам индустрии
- ✅ Готово к production
- ✅ Легко добавить Docker

### 3. **Удобство разработки**
- ✅ Изолированные тесты
- ✅ Отдельная документация
- ✅ Чистый корень проекта

### 4. **Импорты**
- ✅ Абсолютные импорты (`from app.bd import User`)
- ✅ Работают из любой директории
- ✅ Совместимы с uvicorn

## 🚀 Как запускать приложение

### Способ 1: Из корня проекта (РЕКОМЕНДУЕТСЯ)

```bash
# Из любой директории
python run.py
```

**Что происходит:**
- Автоматически добавляется `backend/` в PYTHONPATH
- Запускается uvicorn с reload
- Выводится информация о сервере

**Вывод:**
```
🎲 Запуск D&D Application...
📁 Backend path: c:\Users\User\Documents\DnD_Project\backend
🌐 Server: http://localhost:8000
📚 Docs: http://localhost:8000/docs
```

### Способ 2: Через uvicorn (для production)

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Для разработки с reload:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Способ 3: Прямой запуск main.py

```bash
cd backend/app
python main.py
```

⚠️ **Внимание:** Требует правильной настройки PYTHONPATH

## 🧪 Как запускать тесты

### Все тесты находятся в `backend/tests/`

```bash
# Перейти в папку тестов
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
# Открыть в браузере файл:
frontend/test_client.html
```

## 📝 Изменения в коде

### 1. Импорты обновлены на абсолютные

**Было (относительные):**
```python
from bd import User, get_db
from crud import create_user
from auth import create_access_token
```

**Стало (абсолютные):**
```python
from app.bd import User, get_db
from app.crud import create_user
from app.auth import create_access_token
```

### 2. Путь к базе данных обновлен

**Было:**
```python
DATABASE_URL = "sqlite:///./dnd_app.db"
```

**Стало:**
```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'dnd_app.db')}"
```

Теперь база данных находится в `backend/dnd_app.db`

### 3. Добавлены `__init__.py` файлы

```python
# backend/app/__init__.py
"""
D&D Application Backend
Основной пакет приложения
"""
__version__ = "1.0.0"

# backend/tests/__init__.py
"""
Тесты для D&D Application
"""
```

## 🔧 Настройка IDE

### Visual Studio Code

Добавьте в `.vscode/settings.json`:

```json
{
    "python.analysis.extraPaths": [
        "${workspaceFolder}/backend"
    ],
    "python.autoComplete.extraPaths": [
        "${workspaceFolder}/backend"
    ]
}
```

### PyCharm

1. Правый клик на папку `backend`
2. Mark Directory as → Sources Root

## 📦 Установка зависимостей

```bash
# Перейти в папку backend
cd backend

# Создать виртуальное окружение
python -m venv .venv

# Активировать
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Установить зависимости
pip install -r requirements.txt
```

## 🗄️ База данных

### Расположение
```
backend/dnd_app.db
```

### Инициализация

База данных автоматически инициализируется при запуске приложения:

```python
@app.on_event("startup")
async def startup_event():
    init_db()  # Создает таблицы если их нет
```

### Пересоздание базы данных

```bash
cd backend

# Удалить старую БД
rm dnd_app.db  # Linux/Mac
del dnd_app.db  # Windows

# Запустить приложение - БД создастся автоматически
python run.py
```

## 📚 Документация

Вся документация перемещена в папку `docs/`:

```
docs/
├── README.md              # Основная документация
├── QUICKSTART.md          # Быстрый старт
├── API_DOCUMENTATION.md   # API документация
├── FEATURES.md            # Описание функций
├── PROJECT_STATUS.md      # Статус проекта
├── CHECKLIST.md           # Чеклист
└── ... (другие файлы)
```

### Главный README

В корне проекта находится `README.md` с кратким описанием и ссылками на детальную документацию.

## 🐛 Возможные проблемы

### Проблема 1: ModuleNotFoundError: No module named 'app'

**Решение:**
```bash
# Используйте run.py из корня проекта
python run.py

# Или запускайте uvicorn из папки backend
cd backend
uvicorn app.main:app --reload
```

### Проблема 2: База данных не найдена

**Решение:**
```bash
# Проверьте, что база данных в правильном месте
ls backend/dnd_app.db  # Linux/Mac
dir backend\dnd_app.db  # Windows

# Если нет - запустите приложение, она создастся автоматически
python run.py
```

### Проблема 3: Импорты не работают в IDE

**Решение для VS Code:**
```json
// .vscode/settings.json
{
    "python.analysis.extraPaths": ["${workspaceFolder}/backend"]
}
```

**Решение для PyCharm:**
- Правый клик на `backend` → Mark Directory as → Sources Root

### Проблема 4: Тесты не находят модули

**Решение:**
```bash
# Запускайте тесты из папки backend/tests
cd backend/tests
python quick_test.py
```

## ✅ Проверка работоспособности

### 1. Запустите сервер
```bash
python run.py
```

### 2. Проверьте endpoints

```bash
# Главная страница
curl http://localhost:8000/

# Проверка здоровья
curl http://localhost:8000/health

# Swagger документация
# Откройте в браузере: http://localhost:8000/docs
```

### 3. Запустите тесты

```bash
cd backend/tests
python quick_test.py
```

**Ожидаемый результат:**
```
============================================================
  🧪 БЫСТРЫЙ ТЕСТ D&D API
============================================================

📝 Тестовый пользователь:
   Username: test_user_1234
   Email: test_1234@example.com
   Password: TestPass123

============================================================
  1️⃣ Проверка здоровья сервера
============================================================
✅ Сервер работает!

... (остальные тесты)
```

## 🎉 Готово!

Проект успешно реорганизован и готов к использованию!

### Следующие шаги:

1. ✅ Запустите сервер: `python run.py`
2. ✅ Откройте документацию: http://localhost:8000/docs
3. ✅ Запустите тесты: `cd backend/tests && python quick_test.py`
4. ✅ Откройте HTML клиент: `frontend/test_client.html`

### Полезные ссылки:

- **Документация**: `docs/README.md`
- **Быстрый старт**: `docs/QUICKSTART.md`
- **Структура проекта**: `PROJECT_STRUCTURE.md`
- **API документация**: `docs/API_DOCUMENTATION.md`

---

**Версия**: 1.0.0  
**Дата обновления**: 2025  
**Статус**: ✅ Полностью готово