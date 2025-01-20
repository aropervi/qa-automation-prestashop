import time
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pages.contact_page import ContactPage
from utils.config import TestConfig
from utils.file_utils import FileUtils

@pytest.mark.usefixtures("setup_driver")
class TestContactForm:
    
    def test_contact_form_flow(self):
        """Test completo del formulario: primero caso negativo, luego positivo"""
        page = ContactPage(self.driver)
        
        # Arrange - Preparar archivo para el test positivo
        mi_archivo = "test_upload.txt"
        file_path = FileUtils.get_test_file_path(mi_archivo)
        
        # Creamos el archivo si no existe
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Este es un archivo de prueba para el formulario de contacto")
        
        print("\n=== Test con email inválido ===")
        # Act - Primer intento con email inválido
        page.driver.get(TestConfig.BASE_URL)
        time.sleep(2)  # Espera inicial
        page.navigate_to_contact()
        page.fill_contact_form(
            subject_index=1,
            email="emailinvalido",  # Email sin @ ni dominio
            message="Test mensaje con email inválido",
            file_path=None
        )
        
        # Espera para ver el mensaje de error
        print("Esperando 1 segundo para ver el mensaje de error...")
        time.sleep(1)
        
        # Assert del caso negativo
        result = page.get_form_status()
        print(f"Status del formulario: {result['status']} - {result['message']}")
        assert result["status"] == "error", "El formulario no debería aceptar emails inválidos"
        
        print("\n=== Refrescando página para test positivo ===")
        page.driver.refresh()
        time.sleep(2)
        page.switch_to_main_frame()
        
        print("\n=== Test con datos válidos ===")
        page.navigate_to_contact()  # Volvemos a navegar al contacto
        page.fill_contact_form(
            subject_index=1,
            email=TestConfig.TEST_EMAIL,
            message="Este es un mensaje de prueba con archivo adjunto",
            file_path=file_path
        )
        
        # Assert del caso positivo
        result = page.get_form_status()
        assert result["status"] == "success", f"Error en envío: {result['message']}"
        print(f"✓ Éxito: {result['message']}")
        
        # Espera final para ver el resultado
        print("Esperando 3 segundos para ver el resultado final...")
        time.sleep(3)