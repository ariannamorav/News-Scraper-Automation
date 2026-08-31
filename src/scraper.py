from selenium.webdriver.common.by import By


def extraer_noticias(navegador):
    elementos = navegador.find_elements(
        By.XPATH,
        "//article"
    )

    noticias = []

    for elemento in elementos:
        titulo = elemento.find_element(
            By.XPATH,
            "./h2"
        ).text

        descripcion = elemento.find_element(
            By.XPATH,
            "./p"
        ).text

        url = elemento.find_element(
            By.XPATH,
            "./a"
        ).get_attribute("href")

        noticias.append({
            "title": titulo,
            "description": descripcion,
            "url": url
        })

    return noticias