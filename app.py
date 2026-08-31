import json
import time

from flask import (
    Flask,
    render_template,
    request,
    Response
)

from src.browser import crear_navegador
from src.scraper import extraer_noticias
from src.exporter import noticias_a_csv


app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/analizar", methods=["POST"])
def analizar():

    url = request.form.get("url", "").strip()

    if not url:
        return render_template(
            "index.html",
            error="Debes introducir una URL."
        )

    if not url.startswith(("http://", "https://")):
        return render_template(
            "index.html",
            error="La URL debe comenzar con http:// o https://."
        )

    inicio_tiempo = time.perf_counter()

    navegador = crear_navegador(headless=True)

    try:

        navegador.get(url)

        noticias = extraer_noticias(navegador)

    except Exception as error:

        return render_template(
            "index.html",
            error=f"No fue posible analizar la página: {error}"
        )

    finally:

        navegador.quit()

    tiempo_ejecucion = round(
        time.perf_counter() - inicio_tiempo,
        2
    )

    return render_template(
        "resultados.html",
        noticias=noticias,
        url=url,
        tiempo_ejecucion=tiempo_ejecucion
    )


@app.route("/exportar", methods=["POST"])
def exportar():

    noticias_json = request.form.get("noticias", "")

    if not noticias_json:
        return render_template(
            "index.html",
            error="No hay noticias para exportar."
        )

    try:

        noticias = json.loads(noticias_json)

    except json.JSONDecodeError:

        return render_template(
            "index.html",
            error="No fue posible procesar las noticias."
        )

    contenido_csv = noticias_a_csv(noticias)

    return Response(
        contenido_csv,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=noticias.csv"
        }
    )


if __name__ == "__main__":
    app.run(debug=True)