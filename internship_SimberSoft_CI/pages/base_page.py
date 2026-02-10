"""Базовый класс для Page Objects."""

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from internship_SimberSoft_CI.config import Config

class BasePage:
    """Базовый класс для всех Page Objects."""

    def __init__(self, driver):
        """Инициализировать базовую страницу.

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.TIMEOUT)
        self.logger = logging.getLogger(self.__class__.__name__)

    def find_element(self, locator):
        """Найти элемент с ожиданием.

        Args:
            locator: Tuple (By, value) локатор элемента

        Returns:
            WebElement or None
        """
        self.logger.debug("Поиск элемента: %s", locator)
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.logger.debug("Элемент найден: %s", locator)
            return element
        except Exception as error:
            self.logger.error("Не удалось найти элемент %s: %s", locator, error)
            return None

    def click_element(self, locator):
        """Кликнуть по элементу.

        Args:
            locator: Tuple (By, value) локатор элемента

        Returns:
            bool: True если клик успешен
        """
        self.logger.debug("Клик по элементу: %s", locator)
        element = self.find_element(locator)
        if element:
            try:
                element.click()
                self.logger.info("Успешный клик по элементу: %s", locator)
                return True
            except Exception as error:
                self.logger.error("Не удалось кликнуть по элементу %s: %s", locator, error)
                return False
        return False

    def type_text(self, locator, text):
        """Ввести текст в поле.

        Args:
            locator: Tuple (By, value) локатор элемента
            text: Текст для ввода

        Returns:
            bool: True если текст введен успешно
        """
        self.logger.debug("Ввод текста '%s' в элемент: %s", text, locator)
        element = self.find_element(locator)
        if element:
            try:
                element.clear()
                element.send_keys(text)
                self.logger.info("Текст '%s' введен в элемент: %s", text, locator)
                return True
            except Exception as error:
                self.logger.error("Не удалось ввести текст в элемент %s: %s", locator, error)
                return False
        return False

    def get_element_text(self, locator):
        """Получить текст элемента.

        Args:
            locator: Tuple (By, value) локатор элемента

        Returns:
            str: Текст элемента или пустая строка
        """
        self.logger.debug("Получение текста элемента: %s", locator)
        element = self.find_element(locator)
        if element:
            try:
                text = element.text.strip()
                self.logger.debug("Текст элемента %s: %s", locator, text)
                return text
            except Exception as error:
                self.logger.error("Не удалось получить текст элемента %s: %s", locator, error)
                return ""
        return ""

    def is_element_displayed(self, locator):
        """Проверить отображение элемента.

        Args:
            locator: Tuple (By, value) локатор элемента

        Returns:
            bool: True если элемент отображается
        """
        self.logger.debug("Проверка отображения элемента: %s", locator)
        element = self.find_element(locator)
        if element:
            try:
                displayed = element.is_displayed()
                self.logger.debug("Элемент %s отображается: %s", locator, displayed)
                return displayed
            except Exception as error:
                self.logger.error("Ошибка при проверке отображения элемента %s: %s", locator, error)
                return False
        return False

    def open_page(self, url=""):
        """Открыть страницу.

        Args:
            url: Дополнительный путь к URL

        Returns:
            bool: True если страница открыта успешно
        """
        full_url = f"{Config.BASE_URL}/{url}" if url else Config.BASE_URL
        self.logger.info("Открытие страницы: %s", full_url)
        try:
            self.driver.get(full_url)
            self.logger.info("Страница открыта: %s", full_url)
            return True
        except Exception as error:
            self.logger.error("Не удалось открыть страницу %s: %s", full_url, error)
            return False