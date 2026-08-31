from selenium.webdriver.common.by import By


XPATH_NOTICIAS = "//h2[contains(@class, 'Promo-title')]//a"


def extraer_noticias(navegador):
    elementos = navegador.find_elements(
        By.XPATH,
        XPATH_NOTICIAS
    )

    noticias = []

    for elemento in elementos:
        titulo = elemento.text.strip()
        url = elemento.get_attribute("href")

        if not titulo or not url:
            continue

        noticias.append({
            "title": titulo,
            "url": url
        })

    return noticias