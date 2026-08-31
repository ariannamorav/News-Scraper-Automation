from selenium import webdriver


def crear_navegador():
    navegador = webdriver.Chrome()
    return navegador