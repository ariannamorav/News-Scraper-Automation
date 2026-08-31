from selenium import webdriver
from selenium.webdriver.common.by import By

from src.exporter import export_to_csv


def main():
    driver = webdriver.Chrome()

    driver.get("http://localhost:5500/src/test_page.html")

    news_elements = driver.find_elements(
        By.XPATH,
        "//article"
    )

    news = []

    for article in news_elements:

        title = article.find_element(
            By.XPATH,
            "./h2"
        ).text

        description = article.find_element(
            By.XPATH,
            "./p"
        ).text

        url = article.find_element(
            By.XPATH,
            "./a"
        ).get_attribute("href")

        news.append({
            "title": title,
            "description": description,
            "url": url
        })

    driver.quit()

    export_to_csv(
        news,
        "data/noticias.csv"
    )

    print(f"Noticias exportadas: {len(news)}")


if __name__ == "__main__":
    main()