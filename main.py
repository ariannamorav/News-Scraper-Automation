from src.browser import crear_navegador
from src.scraper import extraer_noticias


def main():
    navegador = crear_navegador()

    navegador.get("http://localhost:5500/src/test_page.html")

    noticias = extraer_noticias(navegador)

    navegador.quit()

    print(f"Noticias encontradas: {len(noticias)}")

    for noticia in noticias:
        print(noticia["title"])


if __name__ == "__main__":
    main()