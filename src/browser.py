from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def crear_navegador(headless=False):
    """
    Crea una instancia de Chrome para Selenium.
    """

    opciones = Options()

    if headless:

        opciones.add_argument(
            "--headless=new"
        )

    opciones.add_argument(
        "--window-size=1920,1080"
    )

    opciones.add_argument(
        "--disable-gpu"
    )

    opciones.add_argument(
        "--no-sandbox"
    )

    opciones.add_argument(
        "--disable-dev-shm-usage"
    )

    opciones.add_argument(
        "--disable-notifications"
    )

    opciones.add_argument(
        "--disable-popup-blocking"
    )

    navegador = webdriver.Chrome(
        options=opciones
    )

    return navegador