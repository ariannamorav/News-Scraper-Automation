# News Scraper Automation

Sistema web para la extracción automatizada de noticias a partir de páginas web.

El proyecto permite ingresar la URL de un sitio de noticias, realizar la navegación automatizada mediante Selenium, identificar las noticias disponibles y almacenar los resultados en una base de datos PostgreSQL.

Además de la extracción, la aplicación permite consultar el historial de análisis, revisar el detalle de cada búsqueda, visualizar estadísticas y exportar los resultados obtenidos.

El proyecto fue desarrollado teniendo en cuenta la separación entre aplicación, automatización del navegador y persistencia de datos. Para facilitar su ejecución y evitar dependencias del entorno local, la aplicación y la base de datos están configuradas mediante Docker Compose.

---

## Funcionalidades

### Análisis de páginas

Permite ingresar una URL desde la interfaz web y ejecutar automáticamente el proceso de extracción.

### Extracción automatizada

La navegación y extracción se realizan mediante Selenium y Chromium, evitando depender de una navegación manual.

### Persistencia de información

Los resultados obtenidos se almacenan en PostgreSQL para que puedan ser consultados después de finalizar el análisis.

### Historial

La aplicación conserva los análisis realizados y permite consultar:

- Identificador del análisis.
- URL analizada.
- Fecha del análisis.
- Cantidad de noticias encontradas.

### Detalle de análisis

Cada búsqueda puede abrirse individualmente para consultar todas las noticias obtenidas durante ese análisis.

### Estadísticas

El sistema genera información general a partir de los datos almacenados, incluyendo:

- Total de búsquedas.
- Total de noticias.
- Promedio de noticias por búsqueda.
- Cantidad de noticias agrupadas por dominio.

### Exportación

Los resultados de los análisis pueden exportarse para utilizarlos posteriormente fuera de la aplicación.

### Interfaz web

La aplicación cuenta con una interfaz web desde la cual se pueden realizar análisis y consultar la información almacenada.

---

## Tecnologías utilizadas

### Backend

**Python 3.12**

Lenguaje principal utilizado para desarrollar la aplicación y los módulos de automatización.

**Flask**

Framework utilizado para construir el servidor web, manejar las rutas HTTP, recibir solicitudes y renderizar las interfaces.

### Automatización

**Selenium**

Utilizado para automatizar la navegación del navegador y acceder al contenido de las páginas analizadas.

**Chromium**

Navegador utilizado por Selenium para realizar la navegación automatizada.

**Chromium Driver**

Permite la comunicación entre Selenium y Chromium dentro del contenedor de la aplicación.

### Base de datos

**PostgreSQL 16**

Sistema de gestión de base de datos utilizado para almacenar los análisis y las noticias obtenidas.

### Frontend

**HTML**

Utilizado para construir las diferentes interfaces de la aplicación.

**CSS**

Utilizado para definir el diseño y presentación de la interfaz.

**JavaScript**

Utilizado para agregar comportamiento e interacción en el frontend.

**Bootstrap 5**

Utilizado como apoyo para determinados componentes y estilos de la interfaz.

### Infraestructura

**Docker**

Utilizado para contenerizar la aplicación y establecer un entorno reproducible.

**Docker Compose**

Utilizado para definir y ejecutar conjuntamente los servicios de Flask y PostgreSQL.


---

## Arquitectura del proyecto

La aplicación está organizada en diferentes componentes para separar las responsabilidades.

```text
                    ┌──────────────────────┐
                    │      Navegador       │
                    │       Usuario        │
                    └──────────┬───────────┘
                               │
                               v
                    ┌──────────────────────┐
                    │        Flask         │
                    │       app.py         │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 v                           v
       ┌──────────────────┐        ┌──────────────────┐
       │     Selenium     │        │    PostgreSQL    │
       │    + Chromium    │        │     Database     │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                v                           │
       ┌──────────────────┐                 │
       │      Scraper     │                 │
       │   extracción     │─────────────────┘
       └──────────────────┘
```


## Estructura del proyecto

```text
news-scraper-automation/
│
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
├── README.md
│
├── src/
│   ├── browser.py
│   ├── database.py
│   └── scraper.py
│
├── templates/
│   ├── index.html
│   ├── historial.html
│   ├── detalle.html
│   └── estadisticas.html
│
└── static/
    ├── css/
    │   └── styles.css
    │
    └── js/
        └── script.js
```

---

## Descripción de los principales archivos

### `app.py`

Es el punto de entrada de la aplicación Flask.

Se encarga de:

- Inicializar Flask.
- Crear las tablas de la base de datos.
- Definir las rutas.
- Recibir las solicitudes.
- Validar los datos.
- Ejecutar el proceso de scraping.
- Guardar los resultados.
- Devolver las respuestas.
- Renderizar las interfaces.

Entre las rutas principales se encuentran:

```text
/
POST /analizar
GET /historial
GET /historial/<busqueda_id>
GET /estadisticas
```

---

### `src/browser.py`

Contiene la configuración utilizada para crear el navegador Selenium.

Su responsabilidad principal es preparar Chromium para ejecutarse correctamente, incluyendo el funcionamiento en modo headless dentro del contenedor Docker.

---

### `src/scraper.py`

Contiene la lógica relacionada con la extracción de noticias.

Recibe el navegador y procesa la página para obtener información de las publicaciones encontradas.

La información extraída incluye:

```text
Título
Enlace
Dominio
```

---

### `src/database.py`

Contiene las operaciones relacionadas con PostgreSQL.

Entre sus responsabilidades se encuentran:

- Crear las tablas.
- Guardar nuevos análisis.
- Guardar las noticias.
- Obtener el historial.
- Consultar un análisis específico.
- Obtener estadísticas.

Esto permite mantener separada la lógica de acceso a datos de la lógica principal de Flask.

---

### `templates/`

Contiene las páginas HTML utilizadas por Flask.

```text
index.html
```

Página principal donde se ingresa la URL.

```text
historial.html
```

Muestra los análisis realizados.

```text
detalle.html
```

Muestra las noticias correspondientes a un análisis.

```text
estadisticas.html
```

Muestra las estadísticas generales del sistema.

---

### `static/`

Contiene los recursos utilizados por la interfaz.

```text
static/css/styles.css
```

Contiene los estilos visuales.

```text
static/js/script.js
```

Contiene la lógica JavaScript utilizada en la interfaz.

---

## Base de datos

El proyecto utiliza PostgreSQL 16 para almacenar la información generada por los análisis.

La aplicación crea automáticamente las tablas necesarias cuando inicia.

Esto evita tener que ejecutar manualmente scripts SQL para preparar una instalación nueva.

La información almacenada permite mantener una relación entre:

```text
Búsqueda
   |
   +--- Noticia
   +--- Noticia
   +--- Noticia
   +--- ...
```

De esta manera, cada análisis puede tener múltiples noticias asociadas.

---

## API

Además de la interfaz web, la aplicación cuenta con endpoints que permiten trabajar directamente con los datos.

### Página principal

```http
GET /
```

Muestra la interfaz principal.

---

### Analizar una URL

```http
POST /analizar
```

Recibe una URL y ejecuta el proceso de extracción.

Ejemplo utilizando JSON:

```json
{
    "url": "https://www.teleantioquia.co/noticias"
}
```

Una respuesta exitosa tiene una estructura similar a:

```json
{
    "mensaje": "Análisis realizado correctamente.",
    "busqueda_id": 11,
    "cantidad_noticias": 10,
    "noticias": [
        {
            "titulo": "Título de la noticia",
            "enlace": "https://ejemplo.com/noticia",
            "dominio": "ejemplo.com"
        }
    ]
}
```

---

### Historial

```http
GET /historial
```

Devuelve los análisis realizados anteriormente.

---

### Consultar un análisis

```http
GET /historial/<busqueda_id>
```

Ejemplo:

```http
GET /historial/11
```

Devuelve la información del análisis y las noticias asociadas.

---

### Estadísticas

```http
GET /estadisticas
```

Devuelve las estadísticas generales del sistema.

---

## Docker

Una de las características importantes del proyecto es que el entorno de ejecución está definido mediante Docker.

La aplicación utiliza dos servicios principales:

```text
┌───────────────────────────────┐
│       news-scraper-app        │
│                               │
│ Flask                         │
│ Python                        │
│ Selenium                      │
│ Chromium                      │
│ Chromium Driver               │
└───────────────┬───────────────┘
                │
                │ Red Docker
                │
┌───────────────▼───────────────┐
│      news-scraper-postgres    │
│                               │
│ PostgreSQL 16                 │
└───────────────────────────────┘
```

Esto permite que la aplicación tenga disponibles las dependencias necesarias sin tener que configurar manualmente Python, Chromium o PostgreSQL en el equipo donde se ejecuta.

---

## Dockerfile

El `Dockerfile` define la imagen utilizada para ejecutar la aplicación.

Dentro del contenedor se instala:

- Python.
- Dependencias del proyecto.
- Chromium.
- Chromium Driver.

Después se copia el código de la aplicación al contenedor.

Esto permite ejecutar Flask y Selenium dentro del mismo entorno.

---

## Docker Compose

El archivo `docker-compose.yml` define los servicios utilizados por el proyecto.

Principalmente:

```text
app
postgres
```

El servicio `app` ejecuta la aplicación Flask.

El servicio `postgres` ejecuta PostgreSQL 16.

Docker Compose permite iniciar ambos servicios de forma conjunta:

```bash
docker compose up -d --build
```

---

## Requisitos

Para ejecutar el proyecto utilizando Docker se necesita:

- Docker Desktop
- Git

No es necesario instalar directamente:

- Python
- PostgreSQL
- Chromium
- Chromium Driver

cuando se utiliza la configuración proporcionada por Docker.

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/ariannamorav/News-Scraper-Automation.git
```

Entrar al directorio:

```bash
cd news-scraper-automation
```

---

## Configuración de variables de entorno

Si se utilizan variables de entorno para la configuración de PostgreSQL o Flask, estas deben definirse en un archivo `.env`.

Ejemplo:

```env
POSTGRES_DB=news_scraper
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_clave
```

El archivo `.env` contiene información que depende del entorno de ejecución y no debe subirse al repositorio.

Para facilitar la configuración de nuevos entornos, puede utilizarse un archivo `.env.example` con valores de referencia.

---

## Ejecutar el proyecto

Construir las imágenes y levantar los servicios:

```bash
docker compose up -d --build
```

Comprobar que los contenedores estén funcionando:

```bash
docker compose ps
```

El resultado debería mostrar los servicios de la aplicación y PostgreSQL en ejecución.

Por ejemplo:

```text
news-scraper-app
news-scraper-postgres
```

---

## Acceder a la aplicación

Una vez iniciados los contenedores, abrir:

```text
http://localhost:5000
```

La página principal permite ingresar una URL y comenzar un análisis.

---

## Comprobar los logs

Para consultar los registros de Flask:

```bash
docker compose logs app
```

Para consultar las últimas líneas:

```bash
docker compose logs app --tail=50
```

Para consultar los registros de PostgreSQL:

```bash
docker compose logs postgres
```

---

## Detener la aplicación

Para detener los servicios:

```bash
docker compose down
```

Para iniciar nuevamente los contenedores:

```bash
docker compose up -d
```

Si se realizaron cambios en el código y es necesario reconstruir la imagen:

```bash
docker compose up -d --build
```

---

## Verificación del funcionamiento

Después de iniciar Docker Compose se puede comprobar el estado de los servicios con:

```bash
docker compose ps
```

La aplicación debe aparecer como `Up` y PostgreSQL debe aparecer como `healthy`.

También se puede comprobar directamente la aplicación desde:

```text
http://localhost:5000
```

Si Flask está funcionando correctamente, la interfaz principal será cargada desde `templates/index.html`.

---

## Resultados del proyecto

El sistema permite completar el flujo completo desde la recepción de una URL hasta el almacenamiento y consulta de los resultados:

```text
URL
 |
 v
Solicitud HTTP
 |
 v
Flask
 |
 v
Selenium
 |
 v
Chromium
 |
 v
Extracción
 |
 v
PostgreSQL
 |
 +-------> Historial
 |
 +-------> Detalle
 |
 +-------> Estadísticas
 |
 +-------> Exportación
```

Esto integra diferentes áreas del desarrollo de software dentro de una misma aplicación:

- Desarrollo backend.
- Automatización web.
- Extracción de información.
- Manejo de bases de datos.
- Desarrollo frontend.
- Diseño de API.
- Contenedorización.
- Control de versiones.

---

## Limitaciones actuales

El scraper depende de la estructura HTML de las páginas que analiza. Si un sitio cambia significativamente su estructura, los selectores utilizados pueden necesitar modificaciones.

También existen sitios que pueden implementar mecanismos contra bots o automatización, por lo que Selenium no garantiza que todas las páginas puedan ser procesadas de la misma manera.

El proyecto está orientado principalmente a fines académicos, de aprendizaje y demostración técnica.

---

## Posibles mejoras

Como siguientes etapas del proyecto se podrían incorporar:

- Soporte para diferentes estructuras de páginas de noticias.
- Configuración de la cantidad máxima de noticias a extraer.
- Filtros por dominio.
- Filtros por fecha.
- Búsqueda dentro del historial.
- Paginación.
- Autenticación de usuarios.
- Programación de análisis automáticos.
- Sistema de notificaciones.
- Registro más detallado de errores.
- Procesamiento de múltiples fuentes.
- Dashboard con gráficos.
- Ejecución de tareas programadas mediante un sistema de colas.

---

## Estado actual

Actualmente el proyecto cuenta con:

- Aplicación web funcional.
- Interfaz para ingresar URLs.
- Extracción automatizada mediante Selenium.
- Chromium integrado en el entorno Docker.
- Persistencia de información en PostgreSQL.
- Historial de análisis.
- Consulta de detalles.
- Estadísticas generales.
- Exportación de resultados.
- API para las operaciones principales.
- Dockerfile para la aplicación.
- Docker Compose para la aplicación y PostgreSQL.
- Configuración de `.gitignore` y `.dockerignore`.
- Estructura modular del código.

---
