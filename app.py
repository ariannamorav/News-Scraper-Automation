import os
import csv
import io

from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    Response
)

from src.database import (
    crear_tablas,
    guardar_busqueda,
    obtener_historial,
    obtener_busqueda,
    obtener_estadisticas
)

from src.browser import crear_navegador
from src.scraper import extraer_noticias


# ============================================================
# CONFIGURACIÓN
# ============================================================

app = Flask(__name__)

HOST = os.getenv(
    "FLASK_HOST",
    "0.0.0.0"
)

PORT = int(
    os.getenv(
        "FLASK_PORT",
        "5000"
    )
)

DEBUG = (
    os.getenv(
        "FLASK_DEBUG",
        "0"
    ) == "1"
)


# ============================================================
# INICIALIZAR BASE DE DATOS
# ============================================================

crear_tablas()


# ============================================================
# RUTA PRINCIPAL - INTERFAZ
# ============================================================

@app.route("/", methods=["GET"])
def inicio():
    """
    Muestra la interfaz principal del sistema.
    """

    return render_template(
        "index.html"
    )


# ============================================================
# ANALIZAR UNA URL
# ============================================================

@app.route("/analizar", methods=["POST"])
def analizar():
    """
    Recibe una URL desde el formulario web o mediante JSON.

    Ejecuta Selenium,
    extrae las noticias
    y guarda el resultado en PostgreSQL.
    """

    # --------------------------------------------------------
    # RECIBIR DATOS
    # --------------------------------------------------------

    datos = request.get_json(
        silent=True
    )

    if datos is not None:

        url = datos.get(
            "url"
        )

    else:

        url = request.form.get(
            "url"
        )


    # --------------------------------------------------------
    # VALIDAR URL
    # --------------------------------------------------------

    if not url:

        return jsonify({

            "error":
                "La URL es obligatoria."

        }), 400


    url = url.strip()


    if not url:

        return jsonify({

            "error":
                "La URL es obligatoria."

        }), 400


    navegador = None


    try:

        # ----------------------------------------------------
        # CREAR NAVEGADOR
        # ----------------------------------------------------

        navegador = crear_navegador(
            headless=True
        )


        # ----------------------------------------------------
        # ABRIR URL
        # ----------------------------------------------------

        navegador.get(
            url
        )


        # ----------------------------------------------------
        # EXTRAER NOTICIAS
        # ----------------------------------------------------

        noticias = extraer_noticias(
            navegador
        )


        # ----------------------------------------------------
        # GUARDAR BÚSQUEDA
        # ----------------------------------------------------

        busqueda_id = guardar_busqueda(
            url,
            noticias
        )


        # ----------------------------------------------------
        # RESPUESTA
        # ----------------------------------------------------

        return jsonify({

            "mensaje":
                "Análisis realizado correctamente.",

            "busqueda_id":
                busqueda_id,

            "url":
                url,

            "cantidad_noticias":
                len(noticias),

            "noticias":
                noticias

        }), 200


    except Exception as error:

        return jsonify({

            "error":
                "No fue posible realizar el análisis.",

            "detalle":
                str(error)

        }), 500


    finally:

        if navegador:

            try:

                navegador.quit()

            except Exception:

                pass


# ============================================================
# HISTORIAL - API
# ============================================================

@app.route(
    "/historial",
    methods=["GET"]
)
def historial():
    """
    Devuelve todas las búsquedas realizadas.
    """

    try:

        resultados = obtener_historial()


        return jsonify({

            "total":
                len(resultados),

            "historial":
                resultados

        }), 200


    except Exception as error:

        return jsonify({

            "error":
                "No fue posible obtener el historial.",

            "detalle":
                str(error)

        }), 500


# ============================================================
# HISTORIAL - INTERFAZ WEB
# ============================================================

@app.route(
    "/historial-ui",
    methods=["GET"]
)
def historial_ui():
    """
    Muestra el historial mediante la interfaz web.
    """

    try:

        resultados = obtener_historial()


        return render_template(

            "historial.html",

            historial=resultados,

            error=None

        )


    except Exception as error:

        return render_template(

            "historial.html",

            historial=[],

            error=str(error)

        )


# ============================================================
# CONSULTAR UNA BÚSQUEDA - API
# ============================================================

@app.route(
    "/historial/<int:busqueda_id>",
    methods=["GET"]
)
def consultar_busqueda(busqueda_id):
    """
    Devuelve una búsqueda específica
    junto con sus noticias.
    """

    try:

        resultado = obtener_busqueda(
            busqueda_id
        )


        if resultado is None:

            return jsonify({

                "error":
                    "La búsqueda no existe.",

                "busqueda_id":
                    busqueda_id

            }), 404


        return jsonify(
            resultado
        ), 200


    except Exception as error:

        return jsonify({

            "error":
                "No fue posible consultar la búsqueda.",

            "detalle":
                str(error)

        }), 500


# ============================================================
# DETALLE - INTERFAZ WEB
# ============================================================

@app.route(
    "/historial-ui/<int:busqueda_id>",
    methods=["GET"]
)
def detalle_ui(busqueda_id):
    """
    Muestra el detalle de una búsqueda
    mediante la interfaz web.
    """

    try:

        resultado = obtener_busqueda(
            busqueda_id
        )


        if resultado is None:

            return render_template(
                "detalle.html",
                resultado=None,
                error="La búsqueda no existe."
            ), 404


        return render_template(

            "detalle.html",

            resultado=resultado,

            error=None

        )


    except Exception as error:

        return render_template(

            "detalle.html",

            resultado=None,

            error=str(error)

        ), 500


# ============================================================
# ESTADÍSTICAS - API
# ============================================================

@app.route(
    "/estadisticas",
    methods=["GET"]
)
def estadisticas():
    """
    Devuelve las estadísticas generales
    del sistema.
    """

    try:

        resultados = obtener_estadisticas()


        return jsonify(
            resultados
        ), 200


    except Exception as error:

        return jsonify({

            "error":
                "No fue posible obtener las estadísticas.",

            "detalle":
                str(error)

        }), 500


# ============================================================
# ESTADÍSTICAS - INTERFAZ WEB
# ============================================================

@app.route(
    "/estadisticas-ui",
    methods=["GET"]
)
def estadisticas_ui():
    """
    Muestra las estadísticas mediante
    la interfaz web.
    """

    try:

        resultados = obtener_estadisticas()


        return render_template(

            "estadisticas.html",

            estadisticas=resultados

        )


    except Exception as error:

        return render_template(

            "estadisticas.html",

            estadisticas={

                "total_busquedas": 0,

                "total_noticias": 0,

                "promedio_noticias": 0,

                "dominios": []

            },

            error=str(error)

        )


# ============================================================
# EXPORTAR ANÁLISIS A CSV
# ============================================================

@app.route(
    "/exportar/<int:busqueda_id>",
    methods=["GET"]
)
def exportar(busqueda_id):
    """
    Exporta las noticias de una búsqueda
    a un archivo CSV compatible con Excel.

    Se utiliza ';' como separador porque
    Excel en configuraciones regionales
    en español normalmente utiliza punto y coma.
    """

    try:

        # ----------------------------------------------------
        # OBTENER BÚSQUEDA
        # ----------------------------------------------------

        resultado = obtener_busqueda(
            busqueda_id
        )


        if resultado is None:

            return jsonify({

                "error":
                    "La búsqueda no existe.",

                "busqueda_id":
                    busqueda_id

            }), 404


        # ----------------------------------------------------
        # CREAR ARCHIVO CSV EN MEMORIA
        # ----------------------------------------------------

        salida = io.StringIO(
            newline=""
        )


        escritor = csv.writer(

            salida,

            delimiter=";",

            quotechar='"',

            quoting=csv.QUOTE_MINIMAL,

            lineterminator="\n"

        )


        # ----------------------------------------------------
        # ENCABEZADOS
        # ----------------------------------------------------

        escritor.writerow([

            "Título",

            "Dominio",

            "Enlace"

        ])


        # ----------------------------------------------------
        # AGREGAR NOTICIAS
        # ----------------------------------------------------

        noticias = resultado.get(
            "noticias",
            []
        )


        for noticia in noticias:

            escritor.writerow([

                noticia.get(
                    "titulo",
                    ""
                ),

                noticia.get(
                    "dominio",
                    ""
                ),

                noticia.get(
                    "enlace",
                    ""
                )

            ])


        # ----------------------------------------------------
        # OBTENER CONTENIDO
        # ----------------------------------------------------

        contenido = salida.getvalue()


        # ----------------------------------------------------
        # AGREGAR BOM UTF-8
        # ----------------------------------------------------
        #
        # Esto permite que Excel reconozca correctamente
        # caracteres como:
        #
        # á é í ó ú ñ ¿ ¡
        #
        # ----------------------------------------------------

        contenido = (
            "\ufeff"
            + contenido
        )


        # ----------------------------------------------------
        # NOMBRE DEL ARCHIVO
        # ----------------------------------------------------

        nombre_archivo = (
            f"analisis_{busqueda_id}.csv"
        )


        # ----------------------------------------------------
        # DEVOLVER ARCHIVO
        # ----------------------------------------------------

        return Response(

            contenido,

            mimetype="text/csv",

            headers={

                "Content-Disposition":
                    f'attachment; filename="{nombre_archivo}"'

            }

        )


    except Exception as error:

        return jsonify({

            "error":
                "No fue posible exportar el archivo.",

            "detalle":
                str(error)

        }), 500


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    app.run(

        host=HOST,

        port=PORT,

        debug=DEBUG

    )