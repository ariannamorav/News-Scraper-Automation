# News Scraper

Aplicación web para extraer titulares y enlaces de páginas de noticias a partir de una URL.

El proyecto utiliza Selenium para la navegación y extracción de datos, y Flask para gestionar la aplicación web y mostrar los resultados.

## Tecnologías

- Python
- Flask
- Selenium
- HTML
- CSS
- Bootstrap
- JavaScript

## Funcionalidades

- Ingreso de una URL desde la interfaz web.
- Extracción de titulares y enlaces.
- Identificación del dominio de cada noticia.
- Validación de URLs y títulos.
- Eliminación de resultados duplicados.
- Exportación de resultados a CSV.
- Interfaz de carga durante el proceso de extracción.

## Estructura

```text
news-scraper-automation/
│
├── app.py
├── requirements.txt
│
├── src/
│   ├── browser.py
│   ├── scraper.py
│   └── exporter.py
│
├── templates/
│   ├── index.html
│   └── resultados.html
│
├── static/
│   └── css/
│       └── styles.css
│
└── data/
