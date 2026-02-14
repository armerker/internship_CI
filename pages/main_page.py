"""Page Object для главной страницы Masters Bookstore."""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class MainPage(BasePage):
    """Page Object главной страницы Masters Bookstore."""

    # Локаторы
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.t-store__filter__input.js-store-filter-search")
    CART_ICON = (By.XPATH, "//div[@class='t706__carticon-wrapper']")
    MENU_BOOKS = (By.XPATH, "//a[@class='t-menu__link-item t-active' and contains(@href, '/books')]")
    MENU_BOOKS_TEXT = (By.XPATH, "//a[contains(text(), 'книги') and @class='t-menu__link-item']")
    SORT_SELECT = (By.CSS_SELECTOR, "select.t-store__sort-select.js-store-filter-sort")
    CATEGORY_ALL = (By.CSS_SELECTOR, "div.t-store__parts-switch-btn-all")
    CATEGORY_ALL_TEXT = (By.XPATH, "//div[text()='Все']")

    def __init__(self, driver):
        """Инициализировать главную страницу.

        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)

    def is_page_loaded(self):
        """Проверить загрузку главной страницы.

        Returns:
            bool: True если страница загружена
        """
        self.logger.info("Проверка загрузки главной страницы")

        checks = [
            ("поле поиска", self.SEARCH_INPUT),
            ("иконка корзины", self.CART_ICON),
            ("меню 'книги'", self.MENU_BOOKS_TEXT),
            ("селект сортировки", self.SORT_SELECT),
        ]

        results = []
        for element_name, locator in checks:
            try:
                element = self.find_element(locator)
                if element and element.is_displayed():
                    results.append(True)
                    self.logger.debug("Элемент '%s' найден и отображается", element_name)
                else:
                    results.append(False)
                    self.logger.warning("Элемент '%s' не отображается", element_name)
            except Exception as error:
                results.append(False)
                self.logger.warning("Элемент '%s' не найден: %s", element_name, error)

        title = self.driver.title
        current_url = self.driver.current_url

        self.logger.info("Заголовок страницы: %s", title)
        self.logger.info("Текущий URL: %s", current_url)

        page_loaded = any(results) and bool(title) and "masters-bookstore" in current_url

        if page_loaded:
            self.logger.info("Главная страница загружена")
        else:
            self.logger.warning("Не все элементы главной страницы загружены")

        return page_loaded

    def search(self, query):
        """Выполнить поиск.

        Args:
            query: Строка для поиска

        Returns:
            bool: True если поиск выполнен успешно
        """
        self.logger.info("Выполнение поиска: '%s'", query)

        search_input = self.find_element(self.SEARCH_INPUT)
        if not search_input:
            self.logger.error("Поле поиска не найдено")
            return False

        try:
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)

            self.logger.info("Поиск '%s' выполнен", query)
            return True

        except Exception as error:
            self.logger.error("Ошибка при поиске: %s", error)
            return False

    def get_search_placeholder(self):
        """Получить placeholder поля поиска.

        Returns:
            str: Placeholder или пустая строка
        """
        element = self.find_element(self.SEARCH_INPUT)
        if element:
            return element.get_attribute("placeholder")
        return ""

    def select_sort_option(self, option_text):
        """Выбрать опцию сортировки.

        Args:
            option_text: Текст опции для выбора

        Returns:
            bool: True если сортировка выбрана успешно
        """
        self.logger.info("Выбор сортировки: %s", option_text)

        sort_select = self.find_element(self.SORT_SELECT)
        if not sort_select:
            self.logger.error("Селект сортировки не найден")
            return False

        try:
            select = Select(sort_select)
            select.select_by_visible_text(option_text)

            self.logger.info("Сортировка '%s' выбрана", option_text)
            return True

        except Exception as error:
            self.logger.error("Ошибка при выборе сортировки: %s", error)
            return False

    def click_category_all(self):
        """Кликнуть на категорию 'Все'.

        Returns:
            bool: True если клик успешен
        """
        return self.click_element(self.CATEGORY_ALL)

    def click_cart_icon(self):
        """Кликнуть на иконку корзины.

        Returns:
            bool: True если клик успешен
        """
        return self.click_element(self.CART_ICON)

    def get_current_sort_text(self):
        """Получить текущую выбранную сортировкуе.

        Returns:
            str: Текст текущей сортировки или пустая строка
        """
        sort_select = self.find_element(self.SORT_SELECT)
        if sort_select:
            select = Select(sort_select)
            return select.first_selected_option.text
        return ""

    def go_to_cart(self):
        """Перейти в корзину.

        Returns:
            bool: True если переход успешен
        """
        self.logger.info("Переход в корзину")
        return self.click_element(self.CART_ICON)