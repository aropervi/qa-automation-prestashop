from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException
import time


class OrderPage(BasePage):
    """Page Object for the purchase process in PrestaShop"""

    # Locators for products and cart
    FIRST_PRODUCT = (By.CSS_SELECTOR, ".product-miniature:first-child a")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button.add-to-cart")
    POPUP_PROCEED_BTN = (By.CSS_SELECTOR, ".cart-content-btn a.btn-primary")
    CHECKOUT_BTN = (By.CSS_SELECTOR, "a.btn.btn-primary")
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".js-cart-line-product-quantity")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert.alert-warning")

    # Locators for personal information
    FIRST_NAME_INPUT = (By.NAME, "firstname")
    LAST_NAME_INPUT = (By.NAME, "lastname")
    EMAIL_INPUT = (By.NAME, "email")

    # Each "Continue" button with its distinct name:
    CONTINUE_BTN_PERSONAL_INFO = (By.CSS_SELECTOR, "button.continue[name='continue']")
    CONTINUE_BTN_ADDRESS = (By.CSS_SELECTOR, "button.continue[name='confirm-addresses']")
    CONTINUE_BTN_SHIPPING = (By.CSS_SELECTOR, "button.continue[name='confirmDeliveryOption']")

    # Checkboxes in the form
    PRIVACY_CHECKBOX = (By.NAME, "customer_privacy")
    TERMS_CONDITIONS_CHECKBOX = (By.NAME, "psgdpr")

    # Locators for address
    ADDRESS_INPUT = (By.NAME, "address1")
    CITY_INPUT = (By.NAME, "city")
    POSTAL_CODE_INPUT = (By.NAME, "postcode")
    PHONE_INPUT = (By.NAME, "phone")
    COUNTRY_SELECT = (By.NAME, "id_country")

    # Locators for payment and confirmation
    PAYMENT_OPTION = (By.ID, "payment-option-2")
    TERMS_CHECKBOX = (By.ID, "conditions_to_approve[terms-and-conditions]")
    PLACE_ORDER_BTN = (By.CSS_SELECTOR, "button.place-order")
    ORDER_CONFIRMATION = (By.CSS_SELECTOR, "#content-hook_order_confirmation")

    def select_product(self, index=0):
        print("\nStarting product selection...")
        product = self.wait.until(EC.presence_of_element_located(self.FIRST_PRODUCT))
        self.scroll_into_view(product)
        product.click()
        print("✓ Clicked on product")

        time.sleep(3)
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN))
        print("✓ Product page loaded (Add to Cart button visible)")

    def add_to_cart(self):
        print("\nAdding product to cart...")
        self.click_button_reliably(*self.ADD_TO_CART_BTN)
        print("✓ Clicked Add to Cart")
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart-content")))
        time.sleep(2)

    def proceed_to_checkout_popup(self):
        print("\nProceeding to checkout from popup...")
        self.click_button_reliably(*self.POPUP_PROCEED_BTN)
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN))
        time.sleep(2)

    def proceed_to_checkout(self):
        print("\nProceeding to checkout...")
        self.click_button_reliably(*self.CHECKOUT_BTN)
        time.sleep(2)

    def fill_personal_info(self, first_name, last_name, email):
        print("\nFilling personal information...")
        self.input_text(*self.FIRST_NAME_INPUT, first_name)
        self.input_text(*self.LAST_NAME_INPUT, last_name)
        self.input_text(*self.EMAIL_INPUT, email)

        self.mark_checkbox_reliably(*self.PRIVACY_CHECKBOX)
        self.mark_checkbox_reliably(*self.TERMS_CONDITIONS_CHECKBOX)

        self.click_button_reliably(*self.CONTINUE_BTN_PERSONAL_INFO)
        print("✓ Personal information completed")

    def fill_address(self, address, city, postal_code, phone, country="France"):
        print("\nFilling address...")
        self.input_text(*self.ADDRESS_INPUT, address)
        self.input_text(*self.CITY_INPUT, city)
        self.input_text(*self.POSTAL_CODE_INPUT, postal_code)
        self.input_text(*self.PHONE_INPUT, phone)

        country_select = Select(self.wait.until(EC.presence_of_element_located(self.COUNTRY_SELECT)))
        country_select.select_by_visible_text(country)

        self.click_continue_address_robustly()
        print("✓ Address completed")

    def click_continue_address_robustly(self):
        """
        Robust click for the address confirmation 'Continue' button.
        """
        attempts = 3
        for attempt in range(1, attempts + 1):
            try:
                button = self.wait.until(
                    EC.element_to_be_clickable(self.CONTINUE_BTN_ADDRESS)
                )
                self.scroll_into_view(button)
                self.action_chains_click(button)
                time.sleep(1)

                current_url = self.driver.current_url
                if "delivery" in current_url.lower():
                    print(f"✓ Address 'Continue' button clicked on attempt #{attempt}")
                    return
            except Exception as e:
                print(f"  - Failed on attempt #{attempt}: {str(e)}")
            time.sleep(2)

        # Fallback with JavaScript
        print("=== Fallback: Attempting JavaScript click for 'Continue' address button ===")
        button_js = self.wait.until(EC.presence_of_element_located(self.CONTINUE_BTN_ADDRESS))
        self.scroll_into_view(button_js)
        self.driver.execute_script("arguments[0].click();", button_js)
        time.sleep(2)

    def select_shipping(self):
        print("\nSelecting the shipping method...")
        self.click_continue_shipping_robustly()
        print("✓ Shipping method selected")

    def click_continue_shipping_robustly(self):
        """
        Robust click for the shipping method 'Continue' button.
        """
        attempts = 3
        for attempt in range(1, attempts + 1):
            try:
                button = self.wait.until(
                    EC.element_to_be_clickable(self.CONTINUE_BTN_SHIPPING)
                )
                self.scroll_into_view(button)
                self.action_chains_click(button)
                time.sleep(1)

                current_url = self.driver.current_url
                if "payment-step" in current_url.lower():
                    print(f"✓ Shipping method 'Continue' button clicked on attempt #{attempt}")
                    return
            except Exception as e:
                print(f"  - Failed on attempt #{attempt}: {str(e)}")
            time.sleep(2)

        # Fallback with JavaScript
        print("=== Fallback: Attempting JavaScript click for 'Continue' shipping button ===")
        button_js = self.wait.until(EC.presence_of_element_located(self.CONTINUE_BTN_SHIPPING))
        self.scroll_into_view(button_js)
        self.driver.execute_script("arguments[0].click();", button_js)
        time.sleep(2)

    def complete_order(self):
        print("\nCompleting order...")
        self.mark_checkbox_reliably(*self.TERMS_CHECKBOX)
        self.click_place_order_robustly()
        print("✓ Order completed")

    def click_place_order_robustly(self):
        """
        Robust click for the 'Place Order' button.
        """
        attempts = 3
        for attempt in range(1, attempts + 1):
            try:
                button = self.wait.until(
                    EC.element_to_be_clickable(self.PLACE_ORDER_BTN)
                )
                self.scroll_into_view(button)
                self.action_chains_click(button)
                time.sleep(1)

                current_url = self.driver.current_url
                if "order-confirmation" in current_url.lower():
                    print(f"✓ 'Place Order' button clicked on attempt #{attempt}")
                    return
            except Exception as e:
                print(f"  - Failed on attempt #{attempt}: {str(e)}")
            time.sleep(2)

        # Fallback with JavaScript
        print("=== Fallback: Attempting JavaScript click for 'Place Order' button ===")
        button_js = self.wait.until(EC.presence_of_element_located(self.PLACE_ORDER_BTN))
        self.scroll_into_view(button_js)
        self.driver.execute_script("arguments[0].click();", button_js)
        time.sleep(2)

    def verify_order_confirmation(self):
        print("\nVerifying order confirmation...")
        confirmation = self.wait.until(EC.presence_of_element_located(self.ORDER_CONFIRMATION))
        return confirmation.is_displayed()

    def get_error_message(self):
        try:
            error_element = self.wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
            return error_element.text
        except:
            return ""