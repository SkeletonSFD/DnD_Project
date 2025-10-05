# 🚀 Быстрый старт D&D приложения

## ✅ Чеклист перед запуском

### 1. Проверка установки Python
```bash
python --version
```
Требуется Python 3.8 или выше.

### 2. Активация виртуального окружения (если используется)
```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.\.venv\Scripts\activate.bat
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

## 🎯 Запуск приложения

### Способ 1: Прямой запуск
```bash
python main.py
```

### Способ 2: Через uvicorn
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

После запуска сервер будет доступен на:
- **Главная страница**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Тестирование

### 1. Тест базы данных
```bash
python test_db.py
```
Проверяет создание пользователей, аутентификацию и CRUD операции.

### 2. Быстрый тест API
```bash
python quick_test.py
```
Тестирует регистрацию, логин и защищенные endpoints.

### 3. Тест Socket.IO (Python клиент)
```bash
python test_socketio_client.py
```
Проверяет WebSocket соединение, комнаты, чат и броски кубиков.

### 4. Тест Socket.IO (HTML клиент)
Откройте файл `test_client.html` в браузере.
Красивый интерфейс для тестирования всех Socket.IO функций.

## 📋 Пошаговая инструкция для первого запуска

### Шаг 1: Запустите сервер
```bash
python main.py
```

Вы должны увидеть:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Шаг 2: Откройте Swagger UI
Перейдите в браузере: http://localhost:8000/docs

### Шаг 3: Зарегистрируйте пользователя
1. Найдите endpoint `POST /api/users/register`
2. Нажмите "Try it out"
3. Введите данные:
```json
{
  "username": "player1",
  "email": "player1@example.com",
  "password": "SecurePass123",
  "confirm_password": "SecurePass123",
  "character_name": "Арагорн"
}
```
4. Нажмите "Execute"
5. Скопируйте `access_token` из ответа

### Шаг 4: Авторизуйтесь в Swagger
1. Нажмите кнопку "Authorize" вверху страницы
2. Введите: `Bearer ваш_токен`
3. Нажмите "Authorize"

### Шаг 5: Протестируйте защищенные endpoints
Теперь вы можете использовать:
- `GET /api/users/me` - получить свой профиль
- `GET /api/users/` - список всех пользователей

### Шаг 6: Протестируйте Socket.IO
1. Откройте `test_client.html` в браузере
2. Вставьте ваш JWT токен
3. Нажмите "Connect"
4. Попробуйте:
   - Присоединиться к комнате
   - Отправить сообщение
   - Бросить кубик

## 🎲 Примеры использования

### Регистрация через curl
```bash
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "wizard",
    "email": "wizard@dnd.com",
    "password": "MagicPass123",
    "confirm_password": "MagicPass123",
    "character_name": "Гэндальф"
  }'
```

### Логин через curl
```bash
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "wizard",
    "password": "MagicPass123"
  }'
```

### Получение профиля через curl
```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer ваш_токен"
```

## 🔧 Устранение неполадок

### Проблема: Порт 8000 занят
**Решение**: Измените порт в `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Проблема: Ошибка импорта модулей
**Решение**: Убедитесь, что все зависимости установлены:
```bash
pip install -r requirements.txt
```

### Проблема: База данных не создается
**Решение**: Удалите `dnd_app.db` и перезапустите:
```bash
Remove-Item dnd_app.db
python main.py
```

### Проблема: Socket.IO не подключается
**Решение**: 
1. Проверьте, что сервер запущен
2. Проверьте JWT токен (он должен быть валидным)
3. Откройте консоль браузера для просмотра ошибок

### Проблема: 401 Unauthorized
**Решение**: 
1. Убедитесь, что токен не истек (срок действия 24 часа)
2. Проверьте формат: `Bearer ваш_токен`
3. Получите новый токен через логин

## 📊 Структура базы данных

После первого запуска создается файл `dnd_app.db` с таблицей `users`:

| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Первичный ключ |
| username | String | Уникальное имя пользователя |
| email | String | Уникальный email |
| hashed_password | String | Хешированный пароль |
| character_name | String | Имя персонажа (опционально) |
| is_active | Boolean | Активен ли пользователь |
| created_at | DateTime | Дата создания |
| updated_at | DateTime | Дата обновления |

## 🎮 Готово к игре!

Теперь ваше D&D приложение полностью настроено и готово к использованию!

### Что дальше?
1. Создайте несколько пользователей
2. Протестируйте чат через Socket.IO
3. Попробуйте броски кубиков
4. Создайте игровые комнаты
5. Пригласите друзей!

## 📚 Дополнительная документация

- [README.md](README.md) - Общая информация о проекте
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Полная документация API
- [DATABASE_INFO.md](DATABASE_INFO.md) - Информация о базе данных
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Обзор проекта
- [SETUP_SUMMARY.md](SETUP_SUMMARY.md) - Детальная настройка

---

**Удачной игры! 🎲🐉**