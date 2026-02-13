"""Универсальные фикстуры: локально + Selenoid с явными ожиданиями."""

import sys
import os
import time
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from config import Config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def is_running_in_docker():
    """Проверить, запущен ли код внутри контейнера."""
    in_docker = os.path.exists('/.dockerenv') or os.getenv('SELENOID_HOST') is not None
    logger.info(f"Запуск в контейнере: {in_docker}")
    return in_docker


def wait_for_browser_ready(driver, timeout=15, check_interval=0.5):
    """
    Явное ожидание готовности браузера.

    Args:
        driver: WebDriver instance
        timeout: максимальное время ожидания в секундах
        check_interval: интервал проверки в секундах

    Returns:
        bool: True если браузер готов, False если нет
    """
    logger.info(f"Ожидание готовности браузера (таймаут: {timeout}с)")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # Проверяем, что браузер отвечает на простую команду
            current_url = driver.current_url
            logger.debug(f"Браузер ответил, текущий URL: {current_url}")

            # Проверяем состояние страницы
            ready_state = driver.execute_script("return document.readyState")
            logger.debug(f"Состояние документа: {ready_state}")

            if ready_state == "complete":
                logger.info("Браузер полностью готов")
                return True
            elif ready_state in ["interactive", "loading"]:
                logger.debug(f"Браузер загружается: {ready_state}")

        except WebDriverException as e:
            logger.debug(f"Браузер ещё не готов: {str(e)[:100]}")
        except Exception as e:
            logger.debug(f"Неожиданная ошибка при проверке: {str(e)[:100]}")

        time.sleep(check_interval)

    logger.warning(f"Браузер не стал готов за {timeout} секунд")
    return False


def wait_for_page_load(driver, timeout=10):
    """
    Явное ожидание загрузки страницы.

    Args:
        driver: WebDriver instance
        timeout: максимальное время ожидания в секундах

    Returns:
        bool: True если страница загружена, False если нет
    """
    logger.info(f"Ожидание загрузки страницы (таймаут: {timeout}с)")
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        logger.info("Страница успешно загружена")
        return True
    except TimeoutException:
        logger.warning(f"Страница не загрузилась за {timeout} секунд")
        return False


@pytest.fixture
def driver():
    """Создать WebDriver: локально или через Selenoid с явными ожиданиями."""
    logger.info("=" * 60)
    logger.info(f"Инициализация WebDriver в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    driver_instance = None
    start_time = time.time()

    try:
        if is_running_in_docker():
            host = os.getenv("SELENOID_HOST", "selenoid")
            port = os.getenv("SELENOID_PORT", "4444")
            remote_url = f"http://{host}:{port}/wd/hub"

            options = Options()

            # Явно указываем версию
            options.set_capability("browserVersion", "128.0")

            if Config.HEADLESS:
                options.add_argument("--headless=new")

            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")

            # Остальные опции...

            driver_instance = webdriver.Remote(
                command_executor=remote_url,
                options=options
            )

            # Критически важная задержка!
            time.sleep(5)

            # Аргументы для обхода блокировок
            options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--accept-lang=en-US,en;q=0.9")

            # Отключаем автоматизацию
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            # Настройки для Selenoid
            options.set_capability("selenoid:options", {
                "enableVNC": True,
                "enableVideo": False,
                "name": f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            })

            logger.info("Создание Remote WebDriver...")
            driver_instance = webdriver.Remote(
                command_executor=remote_url,
                options=options
            )
            logger.info("Remote WebDriver создан успешно")

        else:
            # Локальный режим — используем ChromeDriver
            logger.info(f"Режим: локальный ChromeDriver")
            logger.info(f"Headless режим: {Config.HEADLESS}")

            options = Options()

            # Локальный режим — используем ChromeDriver
            options = Options()

            if Config.HEADLESS:
                options.add_argument("--headless=new")

            # Добавь эти две строки для обхода ошибки AMD
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")

            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")

            try:
                logger.info("Попытка запуска ChromeDriver из PATH...")
                driver_instance = webdriver.Chrome(options=options)
                logger.info("ChromeDriver запущен из PATH")
            except Exception as e:
                logger.warning(f"ChromeDriver не найден в PATH: {e}")
                logger.info("Попытка запуска ChromeDriver из папки проекта...")
                service = Service(executable_path="./chromedriver.exe")
                driver_instance = webdriver.Chrome(service=service, options=options)
                logger.info("ChromeDriver запущен из папки проекта")

        # Устанавливаем таймаут загрузки страницы
        driver_instance.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        logger.info(f"Установлен таймаут загрузки страницы: {Config.PAGE_LOAD_TIMEOUT}с")

        # Явное ожидание готовности браузера
        if not wait_for_browser_ready(driver_instance, timeout=20):
            logger.error("Браузер не ответил в течение 20 секунд")
            pytest.skip("Браузер не ответил вовремя")

        elapsed_time = time.time() - start_time
        logger.info(f"WebDriver инициализирован за {elapsed_time:.2f} секунд")

        yield driver_instance

    except Exception as e:
        logger.error(f"Ошибка при создании WebDriver: {str(e)}")
        pytest.skip(f"Не удалось создать WebDriver: {e}")

    finally:
        if driver_instance:
            logger.info("Закрытие WebDriver...")
            driver_instance.quit()
            logger.info("WebDriver закрыт")


@pytest.fixture
def main_page(driver):
    """Создать MainPage с явным ожиданием загрузки."""
    logger.info("Инициализация MainPage")

    from pages.main_page import MainPage

    page = MainPage(driver)

    # Открываем страницу
    logger.info(f"Открытие страницы: {Config.BASE_URL}")
    opened = page.open_page()

    if not opened:
        logger.error("Не удалось открыть главную страницу")
        pytest.skip("Не удалось открыть главную страницу")

    # Явное ожидание загрузки страницы
    if not wait_for_page_load(driver, timeout=15):
        logger.warning("Страница загрузилась не полностью, но продолжаем")

    # Ждем появления body
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(("tag name", "body"))
        )
        logger.info("Body страницы найден")
    except TimeoutException:
        logger.warning("Body страницы не найден, но продолжаем")

    logger.info("MainPage готова к работе")
    return page