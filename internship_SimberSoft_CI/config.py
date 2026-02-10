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
<<<<<<< HEAD
    HEADLESS = True  # Для Jenkins ставим True
=======
    HEADLESS = True
>>>>>>> e5f891d15e7156da0b26930ef8e55cfbec3c920a

    # Timeouts
    TIMEOUT = 10
    PAGE_LOAD_TIMEOUT = 30

    # Test data
    TEST_SEARCH_QUERY = "искусство"

    # Logging
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Paths
    PROJECT_ROOT = Path(__file__).parent
    LOGS_DIR = PROJECT_ROOT / "logs"


CONFIG = Config()

# Создаем директорию для логов если ее нет
os.makedirs(CONFIG.LOGS_DIR, exist_ok=True)

# Настройка логирования
logging.basicConfig(
    level=CONFIG.LOG_LEVEL,
    format=CONFIG.LOG_FORMAT,
    handlers=[
        logging.FileHandler(CONFIG.LOGS_DIR / "test.log"),
        logging.StreamHandler()
    ]
)

LOGGER = logging.getLogger(__name__)
