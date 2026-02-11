"""Тесты главной страницы Masters Bookstore."""

import logging
import pytest
from selenium.webdriver.common.by import By


class TestMainPage:
    """Тест-сьют для главной страницы."""

    def setup_method(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @pytest.mark.smoke
    def test_page_loads(self, main_page):
        title = main_page.driver.title
        current_url = main_page.driver.current_url

        assert title, "Заголовок не должен быть пустым"
        assert "masters-bookstore.ru" in current_url

    @pytest.mark.smoke
    def test_title_contains_name(self, main_page):
        title = main_page.driver.title
        title_lower = title.lower()

        assert "bookstore" in title_lower

    def test_search_input_exists(self, main_page):
        placeholder = main_page.get_search_placeholder()
        search_input = main_page.find_element(main_page.SEARCH_INPUT)
        has_search = search_input is not None

        if has_search and placeholder:
            assert "поиск" in placeholder.lower() or "search" in placeholder.lower()

        assert has_search, "Поле поиска не найдено на странице"

    def test_cart_icon_exists(self, main_page):
        cart_locator = (By.XPATH, "//div[@class='t706__carticon-wrapper']")
        cart_element = main_page.find_element(cart_locator)
        has_cart = cart_element is not None

        assert has_cart, "Иконка корзины не найдена на странице"

    def test_basic_elements_exist(self, main_page):
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

        assert found_count >= 3, f"Найдено слишком мало элементов: {found_count}"