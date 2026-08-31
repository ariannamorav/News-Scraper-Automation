from urllib.parse import urlparse

from selenium.webdriver.common.by import By


# ============================================================
# SELECTORES
# ============================================================

SELECTORES_NOTICIAS = [
    "//article//a[@href]",
    "//h1//a[@href]",
    "//h2//a[@href]",
    "//h3//a[@href]",
]


# ============================================================
# PALABRAS QUE NO SON NOTICIAS
# ============================================================

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
    "fútbol y más deportes",
    "programa de transparencia",
    "términos y condiciones",
    "terminos y condiciones",
    "política de datos personales",
    "politica de datos personales",
}


# ============================================================
# EXTENSIONES QUE NO SON NOTICIAS
# ============================================================

EXTENSIONES_EXCLUIDAS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".svg",
    ".mp3",
    ".mp4",
    ".zip",
}


# ============================================================
# PALABRAS QUE INDICAN CONTENIDO INSTITUCIONAL
# ============================================================

PALABRAS_INSTITUCIONALES = {
    "política",
    "politica",
    "términos",
    "terminos",
    "manual",
    "programa",
    "transparencia",
    "protección de datos",
    "proteccion de datos",
    "privacidad",
    "cookies",
    "contacto",
    "nosotros",
    "corporativo",
}


# ============================================================
# VALIDAR URL
# ============================================================

def es_url_valida(url):
    """
    Comprueba que la URL sea válida.
    """

    if not url:
        return False

    try:
        resultado = urlparse(url)

        return resultado.scheme in ("http", "https")

    except Exception:
        return False


# ============================================================
# VALIDAR EXTENSIÓN
# ============================================================

def es_enlace_de_noticia(url):
    """
    Comprueba que el enlace no apunte a un archivo
    o recurso que no sea una noticia.
    """

    if not url:
        return False

    try:
        ruta = urlparse(url).path.lower()

        for extension in EXTENSIONES_EXCLUIDAS:

            if ruta.endswith(extension):
                return False

        return True

    except Exception:
        return False


# ============================================================
# LIMPIAR TÍTULO
# ============================================================

def limpiar_titulo(titulo):
    """
    Normaliza los espacios innecesarios.
    """

    if not titulo:
        return ""

    return " ".join(titulo.split())


# ============================================================
# VALIDAR TÍTULO
# ============================================================

def es_titulo_valido(titulo):
    """
    Determina si un texto puede considerarse
    un titular de noticia.
    """

    if not titulo:
        return False

    titulo = limpiar_titulo(titulo)

    # Evitar textos demasiado cortos
    if len(titulo) < 25:
        return False

    titulo_minusculas = titulo.lower()

    # Evitar elementos conocidos de navegación
    if titulo_minusculas in PALABRAS_EXCLUIDAS:
        return False

    # Evitar contenido institucional
    for palabra in PALABRAS_INSTITUCIONALES:

        if palabra in titulo_minusculas:
            return False

    return True


# ============================================================
# OBTENER DOMINIO
# ============================================================

def obtener_dominio(url):
    """
    Obtiene únicamente el dominio de una URL.

    Ejemplo:

    https://www.rcnradio.com/colombia/noticia

    Resultado:

    rcnradio.com
    """

    if not url:
        return ""

    try:

        dominio = urlparse(url).netloc

        if dominio.startswith("www."):
            dominio = dominio[4:]

        return dominio

    except Exception:
        return ""


# ============================================================
# EXTRAER NOTICIAS
# ============================================================

def extraer_noticias(navegador):
    """
    Extrae titulares, enlaces y dominios
    desde una página web.

    Devuelve una lista de diccionarios con:

        titulo
        enlace
        dominio
    """

    noticias = []

    urls_encontradas = set()

    for selector in SELECTORES_NOTICIAS:

        try:

            elementos = navegador.find_elements(
                By.XPATH,
                selector
            )

        except Exception:

            continue

        for elemento in elementos:

            # ------------------------------------------------
            # OBTENER TÍTULO
            # ------------------------------------------------

            try:

                titulo = limpiar_titulo(
                    elemento.text
                )

            except Exception:

                continue

            # ------------------------------------------------
            # OBTENER URL
            # ------------------------------------------------

            try:

                url = elemento.get_attribute(
                    "href"
                )

            except Exception:

                continue

            # ------------------------------------------------
            # VALIDAR TÍTULO
            # ------------------------------------------------

            if not es_titulo_valido(titulo):
                continue

            # ------------------------------------------------
            # VALIDAR URL
            # ------------------------------------------------

            if not es_url_valida(url):
                continue

            # ------------------------------------------------
            # DESCARTAR ARCHIVOS
            # ------------------------------------------------

            if not es_enlace_de_noticia(url):
                continue

            # ------------------------------------------------
            # EVITAR DUPLICADOS
            # ------------------------------------------------

            if url in urls_encontradas:
                continue

            urls_encontradas.add(url)

            # ------------------------------------------------
            # OBTENER DOMINIO
            # ------------------------------------------------

            dominio = obtener_dominio(url)

            # ------------------------------------------------
            # GUARDAR NOTICIA
            # ------------------------------------------------

            noticias.append({
                "titulo": titulo,
                "enlace": url,
                "dominio": dominio
            })

    return noticias