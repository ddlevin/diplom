import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class DashboardPage:
    """Page Object для личного кабинета PoiskKino."""

    API_KEY: tuple = (By.CSS_SELECTOR, ".font-mono.select-all")
    COPY_BUTTON: tuple = (By.XPATH, "//button[contains(text(), 'Копировать')]")
    STATS: tuple = (By.XPATH, "//span[contains(text(), 'Использование API')]")
    UPGRADE_BUTTON: tuple = (By.XPATH, "//a[@href='/tariffs']")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)

    @allure.step("ui. Получить заголовок страницы")
    def get_title(self) -> str:
        return self.driver.title

    @allure.step("ui. Получить текущий URL")
    def get_current_url(self) -> str:
        return self.driver.current_url

    @allure.step("ui. Проверить, что API-ключ виден")
    def is_api_key_visible(self) -> bool:
        element = self.wait.until(EC.visibility_of_element_located(self.API_KEY))
        return element.is_displayed()

    @allure.step("ui. Нажать кнопку копирования API-ключа")
    def click_copy_button(self) -> None:
        button = self.wait.until(EC.element_to_be_clickable(self.COPY_BUTTON))
        button.click()

    @allure.step("ui. Проверить, что статистика видна")
    def is_stats_visible(self) -> bool:
        element = self.wait.until(EC.visibility_of_element_located(self.STATS))
        return element.is_displayed()

    @allure.step("ui. Проверить, что кнопка апгрейда видна")
    def is_upgrade_button_visible(self) -> bool:
        element = self.wait.until(EC.visibility_of_element_located(self.UPGRADE_BUTTON))
        return element.is_displayed()
