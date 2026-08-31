import csv


def export_to_csv(news, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["title", "description", "url"]
        )

        writer.writeheader()
        writer.writerows(news)