import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import TestConfig

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TestConfig.MAX_TIMEOUT)

    def switch_to_main_frame(self, frame_id="framelive"):
        """
        Cambia al iframe principal de la demo PrestaShop.
        """
        self.driver.switch_to.default_content()
        iframe = self.wait.until(EC.presence_of_element_located((By.ID, frame_id)))
        self.driver.switch_to.frame(iframe)

    def scroll_into_view(self, element):
        """
        Desplaza la vista hasta que 'element' sea visible.
        """
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def action_chains_click(self, element):
        """
        Hace clic usando ActionChains (mover ratón, click).
        """
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

    def mark_checkbox_reliably(self, checkbox_by, checkbox_locator, max_attempts=3):
        """
        Intenta marcar un checkbox repetidamente hasta max_attempts.
        Busca el <label> padre y hace clic, verificando que el input se marque.
        """
        for attempt in range(1, max_attempts + 1):
            try:
                checkbox = self.wait.until(EC.presence_of_element_located((checkbox_by, checkbox_locator)))
                self.scroll_into_view(checkbox)

                # Buscamos el label ascendente
                label_parent = checkbox.find_element(By.XPATH, "./ancestor::label")

                # Clic con ActionChains
                self.action_chains_click(label_parent)
                time.sleep(1)

                # Verificamos si quedó marcado
                if checkbox.is_selected():
                    print(f"✓ Checkbox {checkbox_locator} marcado en intento #{attempt}")
                    return
                else:
                    print(f"  - Checkbox {checkbox_locator} NO marcado en intento #{attempt}. Reintentando...")

            except Exception as e:
                print(f"  - Error clickeando checkbox {checkbox_locator} (intento {attempt}): {str(e)}")
                time.sleep(1)

        raise TimeoutException(f"✗ No se pudo marcar el checkbox '{checkbox_locator}' tras {max_attempts} intentos.")

    def click_button_reliably(self, button_by, button_locator, max_attempts=3):
        """
        Hace clic (ActionChains) en un botón, reintentando hasta max_attempts.
        """
        for attempt in range(1, max_attempts + 1):
            try:
                button = self.wait.until(EC.element_to_be_clickable((button_by, button_locator)))
                self.scroll_into_view(button)

                self.action_chains_click(button)
                print(f"✓ Botón '{button_locator}' clickeado en intento #{attempt}")
                time.sleep(1)
                return  # Si no hubo excepción, lo consideramos OK

            except Exception as e:
                print(f"  - Error clickeando botón {button_locator} (intento {attempt}): {str(e)}")
                time.sleep(1)

        raise TimeoutException(f"✗ No se pudo hacer clic en el botón '{button_locator}' tras {max_attempts} intentos.")

    def input_text(self, by, locator, text):
        """
        Localiza un campo de texto, limpia y escribe 'text'.
        """
        element = self.wait.until(EC.presence_of_element_located((by, locator)))
        self.scroll_into_view(element)
        element.clear()
        element.send_keys(text)
        print(f"✓ Texto '{text}' ingresado en: {by}={locator}")

    def get_element_text(self, by, locator):
        element = self.wait.until(EC.presence_of_element_located((by, locator)))
        return element.text
