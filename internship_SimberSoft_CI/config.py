"""Конфигурационные настройки проекта."""

import logging
import os
from pathlib import Path


class Config:
    """Конфигурационные настройки проекта."""

    # URLs
    BASE_URL = "https://www.masters-bookstore.ru/books"

    # Browser settings
    BROWSER = "chrome"
    HEADLESS = True

    # Timeouts
    TIMEOUT = 10
    PAGE_LOAD_TIMEOUT = 30

    # Test data
    TEST_SEARCH_QUERY = "искусство"


CONFIG = Config()

# Создаем директорию для логов если ее нет
os.makedirs("logs", exist_ok=True)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/test.log"),
        logging.StreamHandler()
    ]
)

LOGGER = logging.getLogger(__name__)