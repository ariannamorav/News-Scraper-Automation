import csv
from io import StringIO


def noticias_a_csv(noticias):
    """
    Convierte una lista de noticias en contenido CSV.

    Las columnas utilizadas por la aplicación son:
    - title
    - url
    - domain

    Se utiliza punto y coma como separador para facilitar
    la apertura del archivo directamente en Excel.
    """

    archivo = StringIO()

    fieldnames = [
        "title",
        "url",
        "domain"
    ]

    escritor = csv.DictWriter(
        archivo,
        fieldnames=fieldnames,
        delimiter=";",
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\r\n",
        extrasaction="ignore"
    )

    escritor.writeheader()

    for noticia in noticias:

        fila = {
            "title": noticia.get("title", ""),
            "url": noticia.get("url", ""),
            "domain": noticia.get("domain", "")
        }

        escritor.writerow(fila)

    contenido = archivo.getvalue()

    # BOM para que Excel reconozca correctamente
    # los caracteres UTF-8.
    return "\ufeff" + contenido