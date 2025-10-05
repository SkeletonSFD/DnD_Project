from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

# Путь к базе данных SQLite
# Используем абсолютный путь относительно папки backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'dnd_app.db')}"

# Создание движка базы данных
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},  # Необходимо для SQLite
    echo=True  # Логирование SQL запросов (можно отключить в продакшене)
)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


class User(Base):
    """Модель пользователя в базе данных"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    character_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


def get_db():
    """
    Генератор для получения сессии базы данных.
    Используется как зависимость в FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Инициализация базы данных.
    Создает все таблицы, если они еще не существуют.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ База данных инициализирована успешно!")


def drop_db():
    """
    Удаление всех таблиц из базы данных.
    ВНИМАНИЕ: Используйте с осторожностью!
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Все таблицы удалены из базы данных!")


# Автоматическая инициализация базы данных при импорте модуля
if __name__ == "__main__":
    print("Инициализация базы данных...")
    init_db()
    print("Готово!")