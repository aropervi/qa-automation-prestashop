import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.order_page import OrderPage
from utils.config import TestConfig
import time

@pytest.mark.usefixtures("setup_driver")
class TestOrderFlow:
    """Test cases para el flujo de compra"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup común para todos los tests"""
        self.page = OrderPage(self.driver)
        self.driver.get(TestConfig.BASE_URL)
        self.page.switch_to_main_frame()

    def test_order_flow(self):
        """Test completo: caso positivo y luego caso negativo"""
        # Arrange - Datos de prueba
        test_data = {
            "first_name": "Alberto",
            "last_name": "Roper",
            "email": TestConfig.TEST_EMAIL,
            "address": "Arenales 2020",
            "city": "Test City",
            "postal_code": "12345",
            "phone": "123456789"
        }

        print("\n=== Test con datos válidos ===")
        # Flujo completo positivo
        self.page.select_product(0)
        self.page.add_to_cart()
        self.page.proceed_to_checkout_popup()
        self.page.proceed_to_checkout()
        
        self.page.fill_personal_info(
            test_data["first_name"],
            test_data["last_name"],
            test_data["email"]
        )
        
        self.page.fill_address(
            test_data["address"],
            test_data["city"],
            test_data["postal_code"],
            test_data["phone"]
        )
        
        self.page.select_shipping()
        self.page.complete_order()
        
        # Esperar 5 segundos para ver el resultado final
        time.sleep(5)
        
        # Assert
        assert self.page.verify_order_confirmation(), \
            "No se encontró confirmación del pedido"

        print("\n=== Test con cantidad excesiva (9999) ===")
        # Act - Intento con cantidad inválida
        self.page.select_product(0)
        self.page.add_to_cart()
        self.page.proceed_to_checkout_popup()
        
        # Esperar a que el carrito esté completamente cargado
        time.sleep(8)
        print("Modificando cantidad en carrito...")
        
        # Modificar cantidad a 9999 caracter por caracter
        qty_input = self.page.wait.until(EC.element_to_be_clickable(self.page.QUANTITY_INPUT))
        self.page.scroll_into_view(qty_input)
        for char in "9999":
            qty_input.click()
            qty_input.send_keys(char)
            time.sleep(1)  # Intervalo entre caracteres
        
        # Esperar para ver el mensaje de error
        time.sleep(4)
        print("✓ Cantidad modificada a 9999")
        
        # Intentar proceder con el checkout
        try:
            print("\nIntentando proceder con cantidad inválida...")
            proceed_btn = self.page.wait.until(EC.element_to_be_clickable(self.page.CHECKOUT_BTN))
            self.page.scroll_into_view(proceed_btn)
            proceed_btn.click()
            
            error_msg = self.page.get_error_message()
            assert error_msg and "available purchase order quantity" in error_msg, \
                f"Mensaje de error no encontrado o incorrecto: {error_msg}"
            print(f"✓ Mensaje de error verificado: {error_msg}")
            
        except Exception as e:
            print("⚠ Error durante la verificación. Tomando captura...")
            self.driver.save_screenshot("error_checkout.png")
            print("✓ Captura guardada en error_checkout.png")
            raise