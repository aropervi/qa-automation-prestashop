import time
import os
import pytest
from pages.contact_page import ContactPage
from utils.config import TestConfig
from utils.file_utils import FileUtils

@pytest.mark.usefixtures("setup_driver")
class TestContactForm:
    
    def test_contact_form_flow(self):
        """Test completo del formulario: primero caso negativo, luego positivo"""
        page = ContactPage(self.driver)
        
        # Arrange - Crear un archivo de prueba simple
        test_content = "Este es un archivo de prueba para el formulario de contacto"
        file_path = FileUtils.get_test_file_path("test_upload.txt")
        
        # Asegurarnos que el directorio existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Crear el archivo de prueba
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(test_content)
            
        try:
            print("\n=== Test con email inválido ===")
            # Act - Primer intento con email inválido
            page.driver.get(TestConfig.BASE_URL)
            time.sleep(2)  # Espera adicional para CI
            page.navigate_to_contact()
            page.fill_contact_form(
                subject_index=1,
                email="emailinvalido",  # Email sin @ ni dominio
                message="Test mensaje con email inválido",
                file_path=None
            )
            
            # Espera para ver el mensaje de error
            print("Esperando por mensaje de error...")
            time.sleep(1)
            
            # Assert del caso negativo
            result = page.get_form_status()
            print(f"Status del formulario: {result['status']} - {result['message']}")
            assert result["status"] == "error", "El formulario no debería aceptar emails inválidos"
            
            print("\n=== Refrescando página para test positivo ===")
            page.driver.refresh()
            time.sleep(2)  # Espera adicional para CI
            page.switch_to_main_frame()
            
            print("\n=== Test con datos válidos ===")
            page.navigate_to_contact()
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
            
        finally:
            # Limpieza: eliminar archivo de prueba
            try:
                os.remove(file_path)
                print(f"✓ Archivo de prueba eliminado: {file_path}")
            except:
                print(f"⚠ No se pudo eliminar el archivo: {file_path}")