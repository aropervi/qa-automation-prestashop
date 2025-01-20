from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time

class ContactPage(BasePage):
    """
    Page Object para el formulario de contacto de PrestaShop.
    """
    # Locators
    CONTACT_LINK = (By.ID, "contact-link")
    SUBJECT_DROPDOWN = (By.NAME, "id_contact")
    EMAIL_INPUT = (By.NAME, "from")
    MESSAGE_INPUT = (By.NAME, "message")
    FILE_UPLOAD = (By.NAME, "fileUpload")
    SUBMIT_BUTTON = (By.NAME, "submitMessage")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    # Nuevo locator para mensajes de validación frontend
    FRONTEND_ERROR = (By.CSS_SELECTOR, ".form-error, .alert")  # Ajusta esto según los selectores reales

    def navigate_to_contact(self):
        """Navega a la página de contacto"""
        self.switch_to_main_frame()
        self.click_button_reliably(*self.CONTACT_LINK)
        print("✓ Navegación a página de contacto")

    def fill_contact_form(self, subject_index, email, message, file_path=None):
        """
        Rellena el formulario de contacto
        subject_index: índice del asunto en el dropdown (1: Customer service, 2: Webmaster)
        """
        try:
            # Seleccionar asunto
            if subject_index is not None:
                subject = self.wait.until(EC.presence_of_element_located(self.SUBJECT_DROPDOWN))
                subject.click()
                subject.send_keys(f"{subject_index}")
                print(f"✓ Asunto seleccionado: {subject_index}")

            # Email y mensaje
            self.input_text(*self.EMAIL_INPUT, email)
            self.input_text(*self.MESSAGE_INPUT, message)

            # Subir archivo si se proporciona
            if file_path:
                file_input = self.wait.until(EC.presence_of_element_located(self.FILE_UPLOAD))
                file_input.send_keys(file_path)
                print(f"✓ Archivo subido: {file_path}")

            # Enviar formulario
            self.click_button_reliably(*self.SUBMIT_BUTTON)
            print("✓ Formulario enviado")
            time.sleep(2)  # Esperamos a que se procese el envío

        except Exception as e:
            print(f"✗ Error en fill_contact_form: {str(e)}")
            raise

    def get_form_status(self):
        """
        Retorna el mensaje de éxito o error del formulario.
        Captura específicamente el mensaje de validación del email.
        """
        # Verificamos si hay mensaje de error en el campo email
        try:
            email_field = self.driver.find_element(*self.EMAIL_INPUT)
            validation_message = email_field.get_attribute("validationMessage")
            if validation_message:
                print(f"✓ Mensaje de error capturado: {validation_message}")
                return {"status": "error", "message": validation_message}
        except Exception as e:
            print(f"Error al verificar validación: {str(e)}")

        # Si no hay error de validación, buscamos mensaje de éxito
        try:
            success = self.wait.until(EC.presence_of_element_located(self.SUCCESS_MESSAGE))
            return {"status": "success", "message": success.text}
        except TimeoutException:
            return {"status": "error", "message": "Form validation failed"}