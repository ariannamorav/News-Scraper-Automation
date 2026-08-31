import csv
from io import StringIO


def noticias_a_csv(noticias):

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

        escritor.writerow({
            "title": noticia.get("title", ""),
            "url": noticia.get("url", ""),
            "domain": noticia.get("domain", "")
        })

    return "\ufeff" + archivo.getvalue()