"""
Главный файл FastAPI приложения для оценки кредитных рисков.
"""

import logging
import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Добавляем корневую директорию в путь для импорта конфигурации
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from app.api.routes import router
from app.database import engine, Base

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Создание приложения
app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=config.CORS_ALLOW_METHODS,
    allow_headers=config.CORS_ALLOW_HEADERS,
)

# Создание таблиц базы данных
@app.on_event("startup")
async def startup_event():
    """Создание таблиц при запуске приложения."""
    Base.metadata.create_all(bind=engine)
    logger.info("База данных инициализирована")

# Подключение роутеров
app.include_router(router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Глобальный обработчик исключений.
    
    Args:
        request: HTTP запрос
        exc: Исключение
        
    Returns:
        JSONResponse с информацией об ошибке
    """
    logger.error(f"Необработанное исключение: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Внутренняя ошибка сервера",
            "error": str(exc) if config.LOG_LEVEL == "DEBUG" else "Ошибка обработки запроса"
        }
    )


@app.get("/")
async def root() -> dict:
    """
    Корневой endpoint.
    
    Returns:
        Словарь с информацией о API
    """
    return {
        "message": config.APP_TITLE,
        "version": config.APP_VERSION,
        "docs": "/docs",
        "health": "/api/health",
        "models": ["Altman Z-score", "Taffler"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.API_RELOAD
    )
