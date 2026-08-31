from urllib.parse import urlparse

from selenium.webdriver.common.by import By


SELECTORES_NOTICIAS = [
    "//h2[contains(@class, 'Promo-title')]//a",
    "//article//h1//a",
    "//article//h2//a",
    "//article//h3//a",
    "//h1//a",
    "//h2//a",
    "//h3//a",
]


PALABRAS_EXCLUIDAS = {
    "inicio",
    "home",
    "contacto",
    "contact",
    "login",
    "iniciar sesión",
    "registrarse",
    "registrar",
    "suscríbete",
    "suscribete",
    "menú",
    "menu",
    "buscar",
    "search",
}


def es_url_valida(url):
    """
    Comprueba que la URL tenga un protocolo válido.
    """

    if not url:
        return False

    try:
        resultado = urlparse(url)

        return resultado.scheme in ("http", "https")

    except Exception:
        return False


def es_titulo_valido(titulo):
    """
    Comprueba que el texto tenga características
    mínimas para considerarse un titular.
    """

    if not titulo:
        return False

    titulo = " ".join(titulo.split())

    if len(titulo) < 15:
        return False

    titulo_minusculas = titulo.lower()

    if titulo_minusculas in PALABRAS_EXCLUIDAS:
        return False

    return True


def limpiar_titulo(titulo):
    """
    Normaliza espacios innecesarios del titular.
    """

    return " ".join(titulo.split())


def extraer_noticias(navegador):
    """
    Extrae títulos y enlaces de una página web.

    Se prueban diferentes selectores XPath y posteriormente
    se validan y limpian los resultados.
    """

    noticias = []
    urls_encontradas = set()

    for selector in SELECTORES_NOTICIAS:

        elementos = navegador.find_elements(
            By.XPATH,
            selector
        )

        for elemento in elementos:

            titulo = limpiar_titulo(
                elemento.text
            )

            url = elemento.get_attribute("href")


            # Validar título

            if not es_titulo_valido(titulo):
                continue


            # Validar URL

            if not es_url_valida(url):
                continue


            # Evitar duplicados

            if url in urls_encontradas:
                continue


            urls_encontradas.add(url)


            noticias.append({
                "title": titulo,
                "url": url
            })


    return noticias