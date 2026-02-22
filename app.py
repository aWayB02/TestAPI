from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config import Config
from database.db import init_database
from api.todo_api import router as todo_router

app = FastAPI(
    title=Config.API_TITLE,
    version=Config.API_VERSION,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router)


@app.on_event("startup")
async def startup_event():
    """Инициализация приложения при запуске"""
    init_database()


@app.get("/", tags=["root"])
async def root():
    """
    Корневой эндпоинт приложения

    Returns:
        dict: Приветственное сообщение
    """
    return {
        "message": "Добро пожаловать в To-Do List API",
        "version": Config.API_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Проверка состояния приложения

    Returns:
        dict: Статус приложения
    """
    return {"status": "healthy", "message": "To-Do List API работает нормально"}


if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="127.0.0.1", port=8000, reload=Config.DEBUG, log_level="info"
    )
