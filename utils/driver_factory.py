import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

class DriverFactory:
    @staticmethod
    def get_driver(browser, headless=False):
        """
        Retorna un driver de Selenium según el navegador indicado.
        browser: "chrome" o "firefox"
        headless: bool para ejecutar sin interfaz gráfica
        """
        # Forzar headless en CI
        is_ci = os.getenv('CI') == 'true'
        if is_ci:
            headless = True
            print("[INFO] Ambiente CI detectado - forzando modo headless")

        browser = browser.lower()

        if browser == "chrome":
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            if headless:
                options.add_argument("--headless=new")  # Nueva sintaxis para Chrome
                options.add_argument("--disable-gpu")
                print("[INFO] Modo headless activado para Chrome")
            try:
                print("[INFO] Iniciando ChromeDriver...")
                from webdriver_manager.chrome import ChromeDriverManager
                return webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=options
                )
            except WebDriverException as e:
                raise RuntimeError(f"Error inicializando ChromeDriver: {str(e)}") from e

        elif browser == "firefox":
            from selenium.webdriver.firefox.options import Options
            options = Options()
            if headless:
                options.add_argument("--headless")
                print("[INFO] Modo headless activado para Firefox")
            try:
                print("[INFO] Iniciando GeckoDriver para Firefox...")
                from webdriver_manager.firefox import GeckoDriverManager
                return webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=options
                )
            except WebDriverException as e:
                raise RuntimeError(f"Error inicializando GeckoDriver: {str(e)}") from e

        else:
            raise ValueError(f"Browser '{browser}' no soportado. Usa 'chrome' o 'firefox'.")