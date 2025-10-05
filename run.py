"""
Скрипт для запуска D&D Application из корня проекта
"""
import sys
import os

# Добавляем путь к backend в PYTHONPATH
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Импортируем и запускаем приложение
if __name__ == "__main__":
    import uvicorn
    
    print("🎲 Запуск D&D Application...")
    print(f"📁 Backend path: {backend_path}")
    print("🌐 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )