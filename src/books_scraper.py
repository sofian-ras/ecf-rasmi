import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from settings import BOOKS_BASE_URL, SCRAPER_USER_AGENT, SCRAPER_DELAY, BOOKS_CSV

HEADERS = {"User-Agent": SCRAPER_USER_AGENT}
DELAY = SCRAPER_DELAY

def scrape_books():
    """
    Scrape tous les livres depuis Books to Scrape.
    Retourne une liste de dictionnaires avec image_url.
    """
    books = []
    for idx, book in enumerate(books, start=1):
        book['id'] = idx

    url = urljoin(BOOKS_BASE_URL, "catalogue/page-1.html")

    while url:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erreur HTTP : {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("article", class_="product_pod")

        for item in items:
            title = item.h3.a["title"]
            price_text = item.find("p", class_="price_color").text
            price = price_text.replace("£", "").replace("Â", "").strip()
            availability = item.find("p", class_="instock availability").text.strip()
            rating = item.p["class"][1]

            # Nouvelle ligne pour récupérer l'URL complète de l'image
            img_src = item.find("img")["src"].replace("../../", "")
            image_url = urljoin(BOOKS_BASE_URL, img_src)

            books.append({
                "title": title,
                "price_gbp": float(price),
                "availability": availability,
                "rating": rating,
                "source": "books.toscrape.com",
                "image_url": image_url
            })

        next_btn = soup.find("li", class_="next")
        url = urljoin(url, next_btn.a["href"]) if next_btn else None
        time.sleep(DELAY)

    return books

def save_books_csv(books, filename=BOOKS_CSV):
    """Sauvegarde les livres dans un fichier CSV"""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price_gbp", "availability", "rating", "source", "image_url"])
        writer.writeheader()
        writer.writerows(books)
    print(f"Fichier {filename} créé avec succès !")

if __name__ == "__main__":
    books = scrape_books()
    print(f"Total livres scrapés : {len(books)}")
    save_books_csv(books)
