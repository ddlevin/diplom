import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class LoginPage:
    """Page Object для страницы логина PoiskKino."""

    URL: str = "https://dashboard.poiskkino.dev/login"

    EMAIL_INPUT: tuple = (By.ID, "login-email")
    PASSWORD_INPUT: tuple = (By.ID, "login-password")
    SUBMIT_BUTTON: tuple = (By.CSS_SELECTOR, "button[type='submit']")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=15)

    @allure.step("ui. Открыть страницу логина")
    def open(self) -> None:
        self.driver.get(self.URL)

    @allure.step("ui. Войти с email={email}")
    def login(self, email: str, password: str) -> None:
        email_input = self.wait.until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        )
        email_input.clear()
        email_input.send_keys(email)

        password_input = self.driver.find_element(*self.PASSWORD_INPUT)
        password_input.clear()
        password_input.send_keys(password)

        submit = self.driver.find_element(*self.SUBMIT_BUTTON)
        submit.click()

        self.wait.until(EC.url_contains("/dashboard"))
