from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def crear_navegador(headless=False):
    opciones = Options()

    if headless:
        opciones.add_argument("--headless")

    navegador = webdriver.Chrome(options=opciones)

    return navegador