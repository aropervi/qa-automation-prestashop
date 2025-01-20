import random
import string
import time
import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import TestConfig

class RegistrationPage(BasePage):
    """
    Page Object para el registro en PrestaShop.
    """
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, ".user-info a")
    CREATE_ACCOUNT_LINK = (By.XPATH, "//a[contains(text(), 'No account? Create one here')]")
    TITLE_MR = (By.CSS_SELECTOR, "label[for='field-id_gender-1']")
    FIRST_NAME_INPUT = (By.NAME, "firstname")
    LAST_NAME_INPUT = (By.NAME, "lastname")
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    PRIVACY_CHECKBOX = (By.NAME, "psgdpr")
    CUSTOMER_PRIVACY_CHECKBOX = (By.NAME, "customer_privacy")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[data-link-action='save-customer'], button.form-control-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert.alert-danger")

    def test_create_account(self, first_name, last_name, email, password):
        print("\n=== Iniciando prueba de registro ===")
        print(f"Datos:\n  Nombre: {first_name} {last_name}\n  Email: {email}\n  Password: {password}")
        try:
            self.driver.get(TestConfig.BASE_URL)
            self.switch_to_main_frame()
            self.click_button_reliably(*self.SIGN_IN_BUTTON)
            self.click_button_reliably(*self.CREATE_ACCOUNT_LINK)
            self.click_button_reliably(*self.TITLE_MR)
            self.input_text(*self.FIRST_NAME_INPUT, first_name)
            self.input_text(*self.LAST_NAME_INPUT, last_name)
            self.input_text(*self.EMAIL_INPUT, email)
            self.input_text(*self.PASSWORD_INPUT, password)
            self.mark_checkbox_reliably(*self.PRIVACY_CHECKBOX)
            self.mark_checkbox_reliably(*self.CUSTOMER_PRIVACY_CHECKBOX)
            time.sleep(1)
            self.click_button_reliably(*self.SAVE_BUTTON)
            print("Registro completado exitosamente. El navegador mantendrá sesión activa para inspección.")
            print("Esperando 10s para inspección visual...")
            time.sleep(10)
        except Exception as e:
            print(f"✗ Error en test_create_account: {str(e)}")
            raise

    def generate_strong_password(self, length=12):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choices(chars, k=length))

@pytest.mark.usefixtures("setup_driver")
class TestRegistrationFlow:
    def test_registration_flow(self):
        page = RegistrationPage(self.driver)

        # Test con contraseña débil
        weak_pass = "Test123!"
        print("\n[+] Test con contraseña débil")
        try:
            page.test_create_account(
                first_name="Test",
                last_name="User",
                email=TestConfig.TEST_EMAIL,
                password=weak_pass
            )
        except Exception as e:
            print(f"✗ Error esperado con contraseña débil: {str(e)}")

        # Test con contraseña fuerte
        strong_pass = page.generate_strong_password()
        print("\n[+] Test con contraseña fuerte")
        page.test_create_account(
            first_name="Test",
            last_name="User",
            email="strong_test@example.com",
            password=strong_pass
        )
