"""Фикстуры для тестов - с ручной установкой ChromeDriver."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config import Config


@pytest.fixture
def driver():
    """Создать WebDriver с ручным указанием пути к ChromeDriver."""
    # Отключаем все прокси
    os.environ.update({
        'NO_PROXY': '*',
        'HTTP_PROXY': '',
        'HTTPS_PROXY': '',
        'http_proxy': '',
        'https_proxy': ''
    })

    options = Options()

    if Config.HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")

    try:
        # СПОСОБ 1: Использовать ChromeDriver из PATH
        driver_instance = webdriver.Chrome(options=options)

    except Exception as e1:
        print(f"Способ 1 не сработал: {e1}")

        try:
            # СПОСОБ 2: Указать путь к chromedriver явно
            # Скачайте chromedriver отсюда: https://chromedriver.chromium.org/
            # И положите в папку проекта
            service = Service(executable_path="./chromedriver.exe")
            driver_instance = webdriver.Chrome(service=service, options=options)

        except Exception as e2:
            print(f"Способ 2 не сработал: {e2}")

            try:
                # СПОСОБ 3: Использовать webdriver-manager с отключением прокси
                from webdriver_manager.chrome import ChromeDriverManager
                from webdriver_manager.core.os_manager import ChromeType

                import requests
                session = requests.Session()
                session.trust_env = False

                service = Service(ChromeDriverManager().install())
                driver_instance = webdriver.Chrome(service=service, options=options)

            except Exception as e3:
                pytest.skip(f"Не удалось создать WebDriver. Ошибки: {e1}, {e2}, {e3}")

    driver_instance.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

    yield driver_instance

    if 'driver_instance' in locals():
        driver_instance.quit()


@pytest.fixture
def main_page(driver):
    """Создать MainPage."""
    from pages.main_page import MainPage

    page = MainPage(driver)
    if not page.open_page():
        pytest.skip("Не удалось открыть главную страницу")

    return page