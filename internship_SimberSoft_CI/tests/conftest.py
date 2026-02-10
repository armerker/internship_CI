"""Фикстуры для тестов."""

import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from internship_SimberSoft_CI.config import Config


@pytest.fixture
def driver():
    """Создать и настроить WebDriver.

    Yields:
        WebDriver instance

    Teardown:
        Закрывает браузер
    """
    logger = logging.getLogger("DriverFixture")
    logger.info("Создание WebDriver")

    options = Options()

    if Config.HEADLESS:
        options.add_argument("--headless=new")
        logger.info("Headless режим включен")

    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    try:
        service = Service(ChromeDriverManager().install())
        driver_instance = webdriver.Chrome(service=service, options=options)
        driver_instance.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

        logger.info("WebDriver успешно создан")
        yield driver_instance

    except Exception as error:
        logger.error("Ошибка при создании WebDriver: %s", error)
        raise

    finally:
        logger.info("Закрытие браузера")
        driver_instance.quit()


@pytest.fixture
def main_page(driver):
    """Создать MainPage.

    Args:
        driver: WebDriver instance

    Returns:
        MainPage instance
    """
    from internship_SimberSoft_CI.pages.main_page import MainPage

    logger = logging.getLogger("MainPageFixture")
    logger.info("Создание MainPage")

    page = MainPage(driver)
    if page.open_page():
        logger.info("MainPage успешно создана и открыта")
    else:
        logger.warning("MainPage создана, но открытие страницы не удалось")

    return page