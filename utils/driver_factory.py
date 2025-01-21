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
        # Detectar si estamos en CI y forzar headless
        if os.getenv('CI') == 'true':
            headless = True
            print("[INFO] CI detectado: modo headless activado")

        browser = browser.lower()

        if browser == "chrome":
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--incognito")  # Modo incógnito añadido
            if headless:
                options.add_argument("--headless=new")  # Nueva sintaxis para Chrome
                options.add_argument("--disable-gpu")
            try:
                print("[INFO] Iniciando ChromeDriver en modo incógnito...")
                from webdriver_manager.chrome import ChromeDriverManager
                return webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=options
                )
            except WebDriverException as e:
                raise RuntimeError("Error inicializando ChromeDriver.") from e

        elif browser == "firefox":
            from selenium.webdriver.firefox.options import Options
            options = Options()
            options.add_argument("-private")  # Modo incógnito para Firefox
            if headless:
                options.add_argument("--headless")
            try:
                print("[INFO] Iniciando GeckoDriver para Firefox en modo privado...")
                from webdriver_manager.firefox import GeckoDriverManager
                return webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=options
                )
            except WebDriverException as e:
                raise RuntimeError("Error inicializando GeckoDriver.") from e

        else:
            raise ValueError(f"Browser '{browser}' no soportado. Usa 'chrome' o 'firefox'.")