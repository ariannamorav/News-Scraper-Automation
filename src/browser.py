from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def crear_navegador(headless=False):
    opciones = Options()

    if headless:
        opciones.add_argument("--headless=new")

    opciones.add_argument("--window-size=1920,1080")
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")

    navegador = webdriver.Chrome(options=opciones)

    return navegador