import pytest
from utils.driver_factory import DriverFactory

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="firefox",
        help="Browser a usar para las pruebas (chrome o firefox)."
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecutar en modo headless (sin interfaz gráfica)."
    )

@pytest.fixture(scope="class")
def setup_driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    driver = DriverFactory.get_driver(browser, headless=headless)
    request.cls.driver = driver
    yield
    driver.quit()
