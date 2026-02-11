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
CONFIG_DIR = Path(__file__).parent.absolute()
# Создаем путь к logs относительно config.py
LOGS_DIR = CONFIG_DIR / "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "test.log"),  # Абсолютный путь
        logging.StreamHandler()
    ]
)

LOGGER = logging.getLogger(__name__)