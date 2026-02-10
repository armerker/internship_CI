"""Фикстуры для тестов."""

import sys
import os

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import Config


@pytest.fixture
def driver():
    """Создать и настроить WebDriver.

    Yields:
        WebDriver instance

    Teardown:
        Закрывает браузер
    """
    options = Options()

    if Config.HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-features=VizDisplayCompositor")

    try:
        # Используем правильную версию ChromeDriver для Windows
        service = Service(ChromeDriverManager().install())

        # Добавляем параметры для Windows
        driver_instance = webdriver.Chrome(
            service=service,
            options=options
        )
        driver_instance.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        driver_instance.implicitly_wait(5)

        yield driver_instance

    except Exception as error:
        print(f"Ошибка при создании WebDriver: {error}")
        print(f"Тип ошибки: {type(error)}")
        pytest.skip(f"Не удалось запустить WebDriver: {error}")

    finally:
        if 'driver_instance' in locals():
            try:
                driver_instance.quit()
            except:
                pass


@pytest.fixture
def main_page(driver):
    """Создать MainPage.

    Args:
        driver: WebDriver instance

    Returns:
        MainPage instance
    """
    from pages.main_page import MainPage

    page = MainPage(driver)
    if not page.open_page():
        pytest.fail("Не удалось открыть главную страницу")

    return page