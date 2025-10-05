# 🐛 Исправление ошибки авторизации

## Проблема
При попытке входа в систему возникала ошибка **422 Unprocessable Content**.

```
INFO: 127.0.0.1:63704 - "POST /api/users/login HTTP/1.1" 422 Unprocessable Content
```

### Причина
**Несоответствие форматов данных между фронтендом и backend:**

- **Фронтенд** отправлял данные в формате `application/x-www-form-urlencoded` (OAuth2 стандарт)
- **Backend** ожидал данные в формате JSON через `UserLoginRequest` Pydantic модель

## Решение

### Изменен файл `backend/app/routes_users.py`

#### 1. Добавлен импорт OAuth2PasswordRequestForm:
```python
from fastapi.security import OAuth2PasswordRequestForm
```

#### 2. Изменена сигнатура функции login_user:

**Было:**
```python
@router.post("/login", response_model=TokenResponse)
async def login_user(
    login_data: UserLoginRequest,
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, login_data.username, login_data.password)
```

**Стало:**
```python
@router.post("/login", response_model=TokenResponse)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
```

## Что изменилось?

### OAuth2PasswordRequestForm
Это стандартная FastAPI форма для OAuth2 аутентификации, которая:
- ✅ Принимает данные в формате `application/x-www-form-urlencoded`
- ✅ Совместима со стандартом OAuth2
- ✅ Автоматически парсит поля `username` и `password`
- ✅ Работает с фронтендом, который отправляет `URLSearchParams`

### Преимущества:
1. **Стандартизация** - следует спецификации OAuth2
2. **Совместимость** - работает с любыми OAuth2 клиентами
3. **Автоматическая документация** - Swagger UI правильно отображает форму
4. **Безопасность** - стандартный подход к аутентификации

## Как это работает?

### Фронтенд (frontend/js/auth.js):
```javascript
const formData = new URLSearchParams();
formData.append('username', username);
formData.append('password', password);

const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.LOGIN}`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData
});
```

### Backend (backend/app/routes_users.py):
```python
@router.post("/login", response_model=TokenResponse)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # form_data.username - имя пользователя
    # form_data.password - пароль
    user = authenticate_user(db, form_data.username, form_data.password)
```

## Тестирование

После исправления авторизация работает корректно:

1. Откройте http://localhost:8000/static/index.html
2. Перейдите на вкладку **"Вход"**
3. Заполните форму:
   - **Имя персонажа**: ваше имя пользователя
   - **Секретная фраза**: ваш пароль
4. Нажмите **"Войти в королевство"**

✅ Вход должен пройти успешно, и вы будете перенаправлены в приложение.

## Альтернативный способ тестирования через Swagger UI

1. Откройте http://localhost:8000/docs
2. Найдите endpoint `POST /api/users/login`
3. Нажмите **"Try it out"**
4. Заполните форму:
   - `username`: ваше имя пользователя
   - `password`: ваш пароль
5. Нажмите **"Execute"**

✅ Должен вернуться токен доступа и данные пользователя.

## Статус
✅ **ИСПРАВЛЕНО** - Авторизация работает корректно

## Связанные изменения
- Фронтенд не требует изменений (уже использовал правильный формат)
- Backend теперь соответствует стандарту OAuth2
- Swagger UI теперь правильно отображает форму входа