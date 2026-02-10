"""Тесты поиска на сайте Masters Bookstore."""

import logging
import time
import pytest

from config import Config


class TestSearch:
    """Тест-сьют для функциональности поиска."""

    def setup_method(self):
        """Настройка перед каждым тестом."""
        self.logger = logging.getLogger(self.__class__.__name__)

    @pytest.mark.smoke
    def test_search_works(self, main_page):
        """Проверить что поиск выполняется."""
        self.logger.info("Запуск теста: test_search_works")

        initial_url = main_page.driver.current_url
        self.logger.info("URL до поиска: %s", initial_url)

        search_success = main_page.search(Config.TEST_SEARCH_QUERY)

        if not search_success:
            self.logger.error("Поиск не выполнился")
            assert False, "Поиск не выполнился"

        time.sleep(2)

        new_url = main_page.driver.current_url
        self.logger.info("URL после поиска: %s", new_url)

        assert new_url != initial_url, "URL не изменился после поиска"

        self.logger.info("Тест test_search_works пройден успешно")

    def test_search_with_empty_query(self, main_page):
        """Проверить поиск с пустым запросом."""
        self.logger.info("Запуск теста: test_search_with_empty_query")

        search_success = main_page.search("")

        if not search_success:
            self.logger.warning("Пустой поиск не выполнился")

        assert main_page.is_page_loaded(), "Страница не загружена после пустого поиска"

        self.logger.info("Тест test_search_with_empty_query пройден успешно")

    def test_search_with_special_chars(self, main_page):
        """Проверить поиск со спецсимволами."""
        self.logger.info("Запуск теста: test_search_with_special_chars")

        search_success = main_page.search("@#$%^&*()")

        if not search_success:
            self.logger.warning("Поиск со спецсимволами не выполнился")

        assert main_page.is_page_loaded(), "Страница не загружена после поиска со спецсимволами"

        current_url = main_page.driver.current_url
        assert "masters-bookstore" in current_url, "Сайт перестал работать"

        self.logger.info("Тест test_search_with_special_chars пройден успешно")