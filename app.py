from flask import Flask, request, jsonify, render_template, Response

from src.database import (
    crear_tablas,
    guardar_busqueda,
    obtener_historial,
    obtener_busqueda,
    obtener_estadisticas
)

from src.browser import crear_navegador
from src.scraper import extraer_noticias
from src.exporter import noticias_a_csv


# ============================================================
# CONFIGURACIÓN
# ============================================================

app = Flask(__name__)


# ============================================================
# BASE DE DATOS
# ============================================================

crear_tablas()


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@app.route("/", methods=["GET"])
def inicio():

    return render_template(
        "index.html",
        resultados=None,
        error=None
    )


# ============================================================
# ANALIZAR URL
# ============================================================

@app.route("/analizar", methods=["POST"])
def analizar():

    # --------------------------------------------------------
    # Aceptar JSON o formulario HTML
    # --------------------------------------------------------

    datos_json = request.get_json(silent=True)

    if datos_json:
        url = datos_json.get("url")
        modo_json = True

    else:
        url = request.form.get("url")
        modo_json = False

    # --------------------------------------------------------
    # Validar URL
    # --------------------------------------------------------

    if not url:

        if modo_json:

            return jsonify({
                "error": "La URL es obligatoria."
            }), 400

        return render_template(
            "index.html",
            resultados=None,
            error="La URL es obligatoria."
        ), 400

    navegador = None

    try:

        # ----------------------------------------------------
        # Crear navegador
        # ----------------------------------------------------

        navegador = crear_navegador(headless=True)

        # ----------------------------------------------------
        # Abrir página
        # ----------------------------------------------------

        navegador.get(url)

        # ----------------------------------------------------
        # Extraer noticias
        # ----------------------------------------------------

        noticias = extraer_noticias(navegador)

        # ----------------------------------------------------
        # Guardar búsqueda
        # ----------------------------------------------------

        busqueda_id = guardar_busqueda(
            url,
            noticias
        )

        # ----------------------------------------------------
        # Respuesta API
        # ----------------------------------------------------

        if modo_json:

            return jsonify({
                "mensaje": "Análisis realizado correctamente.",
                "busqueda_id": busqueda_id,
                "url": url,
                "cantidad_noticias": len(noticias),
                "noticias": noticias
            }), 200

        # ----------------------------------------------------
        # Respuesta interfaz
        # ----------------------------------------------------

        resultados = {
            "busqueda_id": busqueda_id,
            "url": url,
            "cantidad_noticias": len(noticias),
            "noticias": noticias
        }

        return render_template(
            "index.html",
            resultados=resultados,
            error=None
        )

    except Exception as error:

        if modo_json:

            return jsonify({
                "error": "No fue posible realizar el análisis.",
                "detalle": str(error)
            }), 500

        return render_template(
            "index.html",
            resultados=None,
            error=f"No fue posible realizar el análisis: {error}"
        ), 500

    finally:

        if navegador:

            try:
                navegador.quit()

            except Exception:
                pass


# ============================================================
# API - HISTORIAL
# ============================================================

@app.route("/historial", methods=["GET"])
def historial():

    try:

        resultados = obtener_historial()

        return jsonify({
            "total": len(resultados),
            "historial": resultados
        }), 200

    except Exception as error:

        return jsonify({
            "error": "No fue posible obtener el historial.",
            "detalle": str(error)
        }), 500


# ============================================================
# INTERFAZ - HISTORIAL
# ============================================================

@app.route("/historial-ui", methods=["GET"])
def historial_ui():

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
        ), 500


# ============================================================
# API - BÚSQUEDA INDIVIDUAL
# ============================================================

@app.route("/historial/<int:busqueda_id>", methods=["GET"])
def consultar_busqueda(busqueda_id):

    try:

        resultado = obtener_busqueda(busqueda_id)

        if resultado is None:

            return jsonify({
                "error": "La búsqueda no existe.",
                "busqueda_id": busqueda_id
            }), 404

        return jsonify(resultado), 200

    except Exception as error:

        return jsonify({
            "error": "No fue posible consultar la búsqueda.",
            "detalle": str(error)
        }), 500


# ============================================================
# INTERFAZ - BÚSQUEDA INDIVIDUAL
# ============================================================

@app.route("/historial-ui/<int:busqueda_id>", methods=["GET"])
def consultar_busqueda_ui(busqueda_id):

    try:

        resultado = obtener_busqueda(busqueda_id)

        if resultado is None:

            return render_template(
                "historial.html",
                historial=[],
                error="La búsqueda no existe."
            ), 404

        return render_template(
            "detalle.html",
            resultado=resultado
        )

    except Exception as error:

        return render_template(
            "historial.html",
            historial=[],
            error=str(error)
        ), 500


# ============================================================
# API - ESTADÍSTICAS
# ============================================================

@app.route("/estadisticas", methods=["GET"])
def estadisticas():

    try:

        resultados = obtener_estadisticas()

        return jsonify(resultados), 200

    except Exception as error:

        return jsonify({
            "error": "No fue posible obtener las estadísticas.",
            "detalle": str(error)
        }), 500


# ============================================================
# INTERFAZ - ESTADÍSTICAS
# ============================================================

@app.route("/estadisticas-ui", methods=["GET"])
def estadisticas_ui():

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
        ), 500


# ============================================================
# EXPORTAR CSV
# ============================================================

@app.route("/exportar/<int:busqueda_id>", methods=["GET"])
def exportar_csv(busqueda_id):

    try:

        resultado = obtener_busqueda(busqueda_id)

        if resultado is None:

            return jsonify({
                "error": "La búsqueda no existe."
            }), 404

        noticias = resultado.get("noticias", [])

        # ----------------------------------------------------
        # Adaptar nombres de campos para el exportador
        # ----------------------------------------------------

        noticias_csv = []

        for noticia in noticias:

            noticias_csv.append({
                "title": noticia.get("titulo", ""),
                "url": noticia.get("enlace", ""),
                "domain": noticia.get("dominio", "")
            })

        contenido = noticias_a_csv(noticias_csv)

        nombre_archivo = f"news_scraper_busqueda_{busqueda_id}.csv"

        return Response(
            contenido.encode("utf-8"),
            mimetype="text/csv; charset=utf-8",
            headers={
                "Content-Disposition":
                    f'attachment; filename="{nombre_archivo}"'
            }
        )

    except Exception as error:

        return jsonify({
            "error": "No fue posible exportar el CSV.",
            "detalle": str(error)
        }), 500


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )