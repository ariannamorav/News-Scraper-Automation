import os

import psycopg


# ============================================================
# CONEXIÓN
# ============================================================

def obtener_conexion():

    return psycopg.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=os.getenv("DB_PORT", "5433"),
        dbname=os.getenv("DB_NAME", "news_scraper"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        client_encoding="UTF8"
    )


# ============================================================
# CREAR TABLAS
# ============================================================

def crear_tablas():

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS busquedas (
                    id SERIAL PRIMARY KEY,
                    url TEXT NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    cantidad_noticias INTEGER DEFAULT 0
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS noticias (
                    id SERIAL PRIMARY KEY,
                    busqueda_id INTEGER NOT NULL,
                    titulo TEXT NOT NULL,
                    enlace TEXT,
                    dominio TEXT,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    CONSTRAINT fk_busqueda
                        FOREIGN KEY (busqueda_id)
                        REFERENCES busquedas(id)
                        ON DELETE CASCADE
                );
            """)

        conexion.commit()

        print("Tablas creadas correctamente.")

    except Exception as error:

        conexion.rollback()

        print("Error al crear las tablas:")
        print(error)

        raise

    finally:

        conexion.close()


# ============================================================
# GUARDAR BÚSQUEDA
# ============================================================

def guardar_busqueda(url, noticias):

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO busquedas (
                    url,
                    cantidad_noticias
                )
                VALUES (%s, %s)
                RETURNING id;
                """,
                (
                    url,
                    len(noticias)
                )
            )

            busqueda_id = cursor.fetchone()[0]

            for noticia in noticias:

                titulo = (
                    noticia.get("titulo")
                    or noticia.get("title")
                    or ""
                )

                enlace = (
                    noticia.get("enlace")
                    or noticia.get("url")
                    or ""
                )

                dominio = (
                    noticia.get("dominio")
                    or noticia.get("domain")
                    or ""
                )

                cursor.execute(
                    """
                    INSERT INTO noticias (
                        busqueda_id,
                        titulo,
                        enlace,
                        dominio
                    )
                    VALUES (%s, %s, %s, %s);
                    """,
                    (
                        busqueda_id,
                        titulo,
                        enlace,
                        dominio
                    )
                )

        conexion.commit()

        print(
            f"Búsqueda guardada correctamente. "
            f"ID: {busqueda_id}. "
            f"Noticias: {len(noticias)}"
        )

        return busqueda_id

    except Exception as error:

        conexion.rollback()

        print("Error al guardar la búsqueda:")
        print(error)

        raise

    finally:

        conexion.close()


# ============================================================
# OBTENER HISTORIAL
# ============================================================

def obtener_historial():

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT
                    id,
                    url,
                    fecha,
                    cantidad_noticias
                FROM busquedas
                ORDER BY fecha DESC, id DESC;
            """)

            filas = cursor.fetchall()

        historial = []

        for fila in filas:

            historial.append({
                "id": fila[0],
                "url": fila[1],
                "fecha": fila[2],
                "cantidad_noticias": fila[3]
            })

        return historial

    finally:

        conexion.close()


# ============================================================
# OBTENER BÚSQUEDA
# ============================================================

def obtener_busqueda(busqueda_id):

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    url,
                    fecha,
                    cantidad_noticias
                FROM busquedas
                WHERE id = %s;
                """,
                (busqueda_id,)
            )

            busqueda = cursor.fetchone()

            if not busqueda:

                return None

            cursor.execute(
                """
                SELECT
                    id,
                    titulo,
                    enlace,
                    dominio,
                    fecha
                FROM noticias
                WHERE busqueda_id = %s
                ORDER BY id DESC;
                """,
                (busqueda_id,)
            )

            filas = cursor.fetchall()

        noticias = []

        for fila in filas:

            noticias.append({
                "id": fila[0],
                "titulo": fila[1],
                "enlace": fila[2],
                "dominio": fila[3],
                "fecha": fila[4]
            })

        return {
            "id": busqueda[0],
            "url": busqueda[1],
            "fecha": busqueda[2],
            "cantidad_noticias": busqueda[3],
            "noticias": noticias
        }

    finally:

        conexion.close()


# ============================================================
# ESTADÍSTICAS
# ============================================================

def obtener_estadisticas():

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            # -----------------------------------------------
            # Totales
            # -----------------------------------------------

            cursor.execute("""
                SELECT
                    COUNT(*) AS total_busquedas,
                    COALESCE(SUM(cantidad_noticias), 0)
                        AS total_noticias,
                    COALESCE(AVG(cantidad_noticias), 0)
                        AS promedio_noticias
                FROM busquedas;
            """)

            totales = cursor.fetchone()

            # -----------------------------------------------
            # Dominios
            # -----------------------------------------------

            cursor.execute("""
                SELECT
                    dominio,
                    COUNT(*) AS cantidad
                FROM noticias
                WHERE dominio IS NOT NULL
                  AND dominio <> ''
                GROUP BY dominio
                ORDER BY cantidad DESC;
            """)

            dominios_filas = cursor.fetchall()

        dominios = []

        for fila in dominios_filas:

            dominios.append({
                "dominio": fila[0],
                "cantidad": fila[1]
            })

        return {
            "total_busquedas": totales[0],
            "total_noticias": totales[1],
            "promedio_noticias": round(
                float(totales[2]), 2
            ),
            "dominios": dominios
        }

    finally:

        conexion.close()