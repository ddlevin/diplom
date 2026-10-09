import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config.config import LOGIN_EMAIL, LOGIN_PASSWORD
from ui.pages.dashboard_page import DashboardPage
from ui.pages.login_page import LoginPage


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    login_page = LoginPage(browser)
    login_page.open()
    login_page.login(LOGIN_EMAIL, LOGIN_PASSWORD)

    yield browser
    browser.quit()


@allure.epic("PoiskKino Dashboard")
@allure.feature("Личный кабинет")
class TestDashboardUI:

    @allure.id("UI-001")
    @allure.story("Загрузка страницы")
    @allure.title("Дашборд загружается после авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_dashboard_loads(self, driver) -> None:
        page = DashboardPage(driver)
        with allure.step("Проверить, что мы на /dashboard"):
            assert "/dashboard" in page.get_current_url()

    @allure.id("UI-002")
    @allure.story("Отображение API-ключа")
    @allure.title("API-ключ отображается на странице")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_key_displayed(self, driver) -> None:
        page = DashboardPage(driver)
        with allure.step("Проверить видимость API-ключа"):
            assert page.is_api_key_visible() is True

    @allure.id("UI-003")
    @allure.story("Кнопка копирования")
    @allure.title("Кнопка копирования API-ключа работает")
    @allure.severity(allure.severity_level.NORMAL)
    def test_copy_button_clickable(self, driver) -> None:
        page = DashboardPage(driver)
        with allure.step("Нажать кнопку 'Копировать'"):
            page.click_copy_button()

    @allure.id("UI-004")
    @allure.story("Статистика")
    @allure.title("Статистика запросов отображается")
    @allure.severity(allure.severity_level.NORMAL)
    def test_stats_visible(self, driver) -> None:
        page = DashboardPage(driver)
        with allure.step("Проверить видимость блока статистики"):
            assert page.is_stats_visible() is True

    @allure.id("UI-005")
    @allure.story("Кнопка апгрейда")
    @allure.title("Кнопка апгрейда тарифа присутствует")
    @allure.severity(allure.severity_level.MINOR)
    def test_upgrade_button_visible(self, driver) -> None:
        page = DashboardPage(driver)
        with allure.step("Проверить видимость ссылки 'Выбрать тариф'"):
            assert page.is_upgrade_button_visible() is True
