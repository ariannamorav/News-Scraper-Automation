from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    driver = webdriver.Chrome()

    driver.get("http://localhost:5500/src/test_page.html")

    news = driver.find_elements(By.XPATH, "//article")

    print(f"Noticias encontradas: {len(news)}")

    for article in news:
        title = article.find_element(By.XPATH, "./h2")
        print(title.text)

    driver.quit()


if __name__ == "__main__":
    main()