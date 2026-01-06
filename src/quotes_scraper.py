import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from settings import QUOTES_BASE_URL, SCRAPER_USER_AGENT, SCRAPER_DELAY, QUOTES_CSV

HEADERS = {"User-Agent": SCRAPER_USER_AGENT}
DELAY = SCRAPER_DELAY

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Erreur HTTP pour {url} : {e}")
        return None

def extract_quotes_from_page(soup, page_url):
    quotes_data = []
    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]
        author_link = quote.find("a", href=True)
        author_url = urljoin(QUOTES_BASE_URL, author_link['href']) if author_link else None

        quotes_data.append({
            "text": text,
            "author": author,
            "tags": ", ".join(tags),
            "author_url": author_url,
            "page_url": page_url,
            "source": "quotes.toscrape.com"
        })

    return quotes_data

def get_next_page_url(soup, current_url):
    next_btn = soup.find("li", class_="next")
    return urljoin(current_url, next_btn.a["href"]) if next_btn else None

def scrape_quotes():
    all_quotes = []
    url = QUOTES_BASE_URL
    page_num = 1

    while url:
        print(f"Scraping page {page_num} : {url}")
        soup = fetch_page(url)
        if not soup:
            break
        quotes = extract_quotes_from_page(soup, url)
        all_quotes.extend(quotes)
        print(f"{len(quotes)} citations extraites")
        url = get_next_page_url(soup, url)
        page_num += 1
        if url:
            time.sleep(DELAY)

    return all_quotes

def save_quotes_csv(quotes, filename=QUOTES_CSV):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags", "author_url", "page_url", "source"])
        writer.writeheader()
        writer.writerows(quotes)
    print(f"Fichier {filename} créé avec succès !")

if __name__ == "__main__":
    quotes = scrape_quotes()
    print(f"Total citations scrapées : {len(quotes)}")
    save_quotes_csv(quotes)
