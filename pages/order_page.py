from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class OrderPage(BasePage):
    """
    Page Object para manejar el carrito y realizar órdenes.
    """
    # Locators
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".add-to-cart")
    CART_ICON = (By.CSS_SELECTOR, ".shopping-cart")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name='qty']")
    PROCEED_TO_CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".checkout")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".cart-total .price")
    CONFIRMATION_MESSAGE = (By.CSS_SELECTOR, ".order-confirmation")

    def add_product_to_cart(self, product_locator):
        product = self.wait.until(EC.element_to_be_clickable(product_locator))
        self.scroll_into_view(product)
        product.click()
        self.click_button_reliably(*self.ADD_TO_CART_BUTTON)
        print("✓ Producto añadido al carrito")
