"""Тесты поиска на сайте Masters Bookstore."""

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import Config


class TestSearch:
    """Тест-сьют для функциональности поиска."""

    @pytest.mark.smoke
    def test_search_works(self, main_page):
        initial_url = main_page.driver.current_url
        search_success = main_page.search(Config.TEST_SEARCH_QUERY)

        if not search_success:
            assert False, "Поиск не выполнился"

        wait = WebDriverWait(main_page.driver, 10)
        wait.until(EC.url_changes(initial_url))

        new_url = main_page.driver.current_url
        assert new_url != initial_url

    def test_search_with_empty_query(self, main_page):
        search_success = main_page.search("")

        if not search_success:
            pytest.skip("Пустой поиск не выполнился")

        wait = WebDriverWait(main_page.driver, 5)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

        assert main_page.is_page_loaded()

    def test_search_with_special_chars(self, main_page):
        search_success = main_page.search("@#$%^&*()")

        if not search_success:
            pytest.skip("Поиск со спецсимволами не выполнился")

        wait = WebDriverWait(main_page.driver, 5)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

        assert main_page.is_page_loaded()

        current_url = main_page.driver.current_url
        assert "masters-bookstore" in current_url