import os
import time
import requests
import pandas as pd
from settings import BOOKS_CSV, QUOTES_CSV, PARTENAIRE_FILE, DATA_DIR, API_ADRESSE_URL, API_USER_AGENT, API_DELAY
from import_excel import import_excel
from books_scraper import scrape_books, save_books_csv
from quotes_scraper import scrape_quotes, save_quotes_csv
from download_images import download_images
from logger import logger

HEADERS = {"User-Agent": API_USER_AGENT}

# créer les dossiers si inexistants
os.makedirs(DATA_DIR, exist_ok=True)

def geocode_partners(file_path):
    partners = pd.read_csv(file_path)

    # ajouter colonnes si manquantes
    if "longitude" not in partners.columns:
        partners["longitude"] = None
    if "latitude" not in partners.columns:
        partners["latitude"] = None

    print("-> Géocodage des partenaires ...")
    for i, row in partners.iterrows():
        adresse_complete = f"{row['adresse']} {row['code_postal']} {row['ville']}"
        try:
            r = requests.get(
                f"{API_ADRESSE_URL}?q={adresse_complete}&limit=1",
                headers=HEADERS,
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            features = data.get("features")
            if features:
                coords = features[0]["geometry"]["coordinates"]
                partners.at[i, "longitude"] = coords[0]
                partners.at[i, "latitude"] = coords[1]
            else:
                partners.at[i, "longitude"] = None
                partners.at[i, "latitude"] = None
        except Exception as e:
            print(f"Erreur géocodage pour {adresse_complete} : {e}")
            partners.at[i, "longitude"] = None
            partners.at[i, "latitude"] = None

        time.sleep(API_DELAY)  # respecter le rate limit

    partners.to_csv(file_path, index=False, encoding="utf-8")
    print("-> Géocodage terminé et CSV mis à jour !")


def extract_all():
    # --- Import fichier partenaire ---
    print("-> Import fichier partenaire ...")
    partenaire_csv = os.path.join(DATA_DIR, "partenaire_librairies_geo.csv")
    import_excel(PARTENAIRE_FILE, partenaire_csv)

    # --- Géocodage ---
    geocode_partners(partenaire_csv)

    # --- Scraping livres ---
    print("-> Scraping livres ...")
    books = scrape_books()
    save_books_csv(books, BOOKS_CSV)
    print("Livres OK :", len(books))

    # --- Télécharger images des livres ---
    download_images(BOOKS_CSV)

    # --- Scraping citations ---
    print("-> Scraping citations ...")
    quotes = scrape_quotes()
    save_quotes_csv(quotes, QUOTES_CSV)
    print("Citations OK :", len(quotes))
