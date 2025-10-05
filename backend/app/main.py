from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

# Импорт роутов и Socket.IO
from app.routes_users import router as users_router
from app.socketio_server import socketio_app, sio
from app.bd import init_db

# Создание FastAPI приложения
app = FastAPI(
    title="D&D Application API",
    description="API для приложения Dungeons & Dragons с поддержкой Socket.IO",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(users_router)

# Монтирование статических файлов (frontend)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    print(f"📁 Frontend path: {frontend_path}")

# Инициализация базы данных при старте
@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске приложения"""
    print("🚀 Запуск D&D приложения...")
    init_db()
    print("✅ База данных инициализирована")
    print("✅ Socket.IO сервер готов")


@app.on_event("shutdown")
async def shutdown_event():
    """Очистка при остановке приложения"""
    print("🛑 Остановка D&D приложения...")


@app.get("/", summary="Главная страница", tags=["Основные"])
def root():
    """Главная страница API"""
    return {
        "message": "🎲 Добро пожаловать в D&D Application API!",
        "version": "1.0.0",
        "docs": "/docs",
        "socketio": "/socket.io",
        "endpoints": {
            "register": "/api/users/register",
            "login": "/api/users/login",
            "me": "/api/users/me",
            "users": "/api/users/"
        }
    }


@app.get("/health", summary="Проверка здоровья", tags=["Основные"])
def health_check():
    """Проверка работоспособности API"""
    return {
        "status": "healthy",
        "database": "connected",
        "socketio": "active"
    }


# Монтирование Socket.IO приложения
app.mount("/", socketio_app)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )