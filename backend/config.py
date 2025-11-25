"""
Конфигурация приложения.
"""

import os
from pathlib import Path
from typing import List

# Базовые пути
BASE_DIR = Path(__file__).parent
APP_DIR = BASE_DIR / "app"

# Настройки API
API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", "8000"))
API_RELOAD: bool = os.getenv("API_RELOAD", "true").lower() == "true"

# Настройки приложения
APP_TITLE: str = "Bankruptcy Risk Assessment API"
APP_DESCRIPTION: str = "API для оценки риска банкротства с использованием моделей Альтмана и Таффлера"
APP_VERSION: str = "2.0.0"

# Настройки логирования
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# CORS настройки
CORS_ORIGINS: List[str] = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:4173,http://localhost:3000"
).split(",")
CORS_ALLOW_CREDENTIALS: bool = True
CORS_ALLOW_METHODS: List[str] = ["*"]
CORS_ALLOW_HEADERS: List[str] = ["*"]
