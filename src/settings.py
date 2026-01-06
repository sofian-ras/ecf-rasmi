import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# --- API ---
API_ADRESSE_URL = "https://api-adresse.data.gouv.fr/search/"
API_USER_AGENT = "ECF-Data-Engineer/1.0"
API_DELAY = 0.05

# --- Scrapers ---
BOOKS_BASE_URL = "https://books.toscrape.com/"
QUOTES_BASE_URL = "https://quotes.toscrape.com/"
SCRAPER_USER_AGENT = "ECF-Data-Engineer/1.0"
SCRAPER_DELAY = 1

# --- Fichiers ---
DATA_DIR = "data/"
PARTENAIRE_FILE = f"{DATA_DIR}partenaire_librairies.xlsx"
BOOKS_CSV = f"{DATA_DIR}books.csv"
QUOTES_CSV = f"{DATA_DIR}quotes.csv"
PARTENAIRE_GEO_CSV = f"{DATA_DIR}partenaire_librairies_geo.csv"

# --- ETL / Output ---
OUTPUT_DIR = "output/"

# --- MinIO ---
MINIO_HOST = os.getenv("MINIO_HOST", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_SECURE = os.getenv("MINIO_SECURE", "False").lower() in ("true", "1", "yes")

