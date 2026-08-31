import csv
from io import StringIO


def noticias_a_csv(noticias):
    archivo = StringIO()

    escritor = csv.DictWriter(
        archivo,
        fieldnames=["title", "url"]
    )

    escritor.writeheader()
    escritor.writerows(noticias)

    return archivo.getvalue()