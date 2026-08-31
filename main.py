from src.browser import crear_navegador
from src.scraper import extraer_noticias
from src.exporter import export_to_csv


def main():
    navegador = crear_navegador(headless=True)

    navegador.get("http://localhost:5500/src/test_page.html")

    noticias = extraer_noticias(navegador)

    navegador.quit()

    export_to_csv(
        noticias,
        "data/noticias.csv"
    )

    print(f"Noticias encontradas: {len(noticias)}")
    print("Archivo CSV generado correctamente.")


if __name__ == "__main__":
    main()