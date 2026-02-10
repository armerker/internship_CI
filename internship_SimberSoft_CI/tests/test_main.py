"""Тесты главной страницы Masters Bookstore."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import pytest
from selenium.webdriver.common.by import By


class TestMainPage:
    """Тест-сьют для главной страницы."""

    def setup_method(self):
        """Настройка перед каждым тестом."""
        self.logger = logging.getLogger(self.__class__.__name__)

    @pytest.mark.smoke
    def test_page_loads(self, main_page):
        """Проверить загрузку главной страницы."""
        self.logger.info("Запуск теста: test_page_loads")

        title = main_page.driver.title
        current_url = main_page.driver.current_url

        self.logger.info("Заголовок: %s", title)
        self.logger.info("URL: %s", current_url)

        assert title, "Заголовок не должен быть пустым"
        assert "masters-bookstore.ru" in current_url

        self.logger.info("Тест test_page_loads пройден успешно")

    @pytest.mark.smoke
    def test_title_contains_name(self, main_page):
        """Проверить что заголовок содержит название магазина."""
        self.logger.info("Запуск теста: test_title_contains_name")

        title = main_page.driver.title
        self.logger.info("Заголовок страницы: %s", title)

        title_lower = title.lower()

        assert "bookstore" in title_lower, f"Заголовок должен содержать 'bookstore'. Заголовок: '{title}'"

        self.logger.info("Тест test_title_contains_name пройден успешно")

    def test_search_input_exists(self, main_page):
        """Проверить наличие поля поиска."""
        self.logger.info("Запуск теста: test_search_input_exists")

        placeholder = main_page.get_search_placeholder()
        self.logger.info("Placeholder поля поиска: '%s'", placeholder)

        search_input = main_page.find_element(main_page.SEARCH_INPUT)
        has_search = search_input is not None

        if has_search:
            self.logger.info("Поле поиска найдено")
            if placeholder:
                assert "поиск" in placeholder.lower() or "search" in placeholder.lower()
        else:
            self.logger.warning("Поле поиска не найдено")

        assert has_search, "Поле поиска не найдено на странице"

        self.logger.info("Тест test_search_input_exists пройден успешно")

    def test_cart_icon_exists(self, main_page):
        """Проверить наличие иконки корзины."""
        self.logger.info("Запуск теста: test_cart_icon_exists")

        cart_locator = (By.XPATH, "//div[@class='t706__carticon-wrapper']")
        cart_element = main_page.find_element(cart_locator)

        has_cart = cart_element is not None

        if has_cart:
            self.logger.info("Иконка корзины найдена")
        else:
            self.logger.warning("Иконка корзины не найдена")

        assert has_cart, "Иконка корзины не найдена на странице"

        self.logger.info("Тест test_cart_icon_exists пройден успешно")

    def test_basic_elements_exist(self, main_page):
        """Проверить наличие базовых элементов."""
        self.logger.info("Запуск теста: test_basic_elements_exist")

        elements_to_check = [
            ("поле поиска", main_page.SEARCH_INPUT),
            ("меню 'книги'", main_page.MENU_BOOKS_TEXT),
            ("селект сортировки", main_page.SORT_SELECT),
            ("категория 'Все'", main_page.CATEGORY_ALL_TEXT),
            ("иконка корзины", main_page.CART_ICON),
        ]

        found_count = 0
        for element_name, locator in elements_to_check:
            element = main_page.find_element(locator)
            if element:
                found_count += 1
                self.logger.info(f"Элемент '{element_name}' найден")
            else:
                self.logger.warning(f"Элемент '{element_name}' не найден")

        self.logger.info("Найдено элементов: %s из %s", found_count, len(elements_to_check))

        assert found_count >= 3, f"Найдено слишком мало элементов: {found_count}"

        self.logger.info("Тест test_basic_elements_exist пройден успешно")