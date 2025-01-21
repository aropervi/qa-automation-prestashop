import pytest
from selenium.webdriver.common.by import By  # Importación corregida
from pages.order_page import OrderPage
from utils.config import TestConfig

@pytest.mark.usefixtures("setup_driver")
class TestOrder:
    
    def test_single_product_order(self):
        """Prueba de realizar una orden con un solo producto."""
        page = OrderPage(self.driver)
        page.driver.get(TestConfig.BASE_URL)

        # Arrange
        product_locator = (By.CSS_SELECTOR, ".product-miniature:first-child")

        # Act
        page.add_product_to_cart(product_locator)
        page.proceed_to_checkout()

        # Assert
        page.validate_order_confirmation()

    def test_multiple_products_order(self):
        """Prueba de realizar una orden con múltiples productos."""
        page = OrderPage(self.driver)
        page.driver.get(TestConfig.BASE_URL)

        # Arrange
        product_locator_1 = (By.CSS_SELECTOR, ".product-miniature:nth-child(1)")
        product_locator_2 = (By.CSS_SELECTOR, ".product-miniature:nth-child(2)")

        # Act
        page.add_product_to_cart(product_locator_1)
        page.add_product_to_cart(product_locator_2)
        page.change_product_quantity(3)  # Cambiar cantidad de uno de los productos
        page.proceed_to_checkout()

        # Assert
        expected_price = "99.99"  # Cambia esto según tu escenario
        page.validate_total_price(expected_price)
        page.validate_order_confirmation()
