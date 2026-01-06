import os
import pandas as pd
from settings import BOOKS_CSV, QUOTES_CSV, PARTENAIRE_GEO_CSV, OUTPUT_DIR
from minio import Minio
from settings import MINIO_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE

os.makedirs(OUTPUT_DIR, exist_ok=True)
GBP_TO_EUR = 1.15

# Connexion MinIO
minio_client = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE
)
bucket_name = "ecf-data"

def transform_all():
    # Livres
    books = pd.read_csv(BOOKS_CSV)
    books["price_eur"] = (books["price_gbp"] * GBP_TO_EUR).round(2)
    books["title"] = books["title"].str.strip()
    books["availability"] = books["availability"].str.strip()
    books.insert(0, "id", range(1, len(books)+1))
    books_file = os.path.join(OUTPUT_DIR, "books_clean.csv")
    books.to_csv(books_file, index=False, encoding="utf-8")
    minio_client.fput_object(bucket_name, "books_clean.csv", books_file)
    print("Books transformés OK")

    # Citations
    quotes = pd.read_csv(QUOTES_CSV)
    quotes["text"] = quotes["text"].str.strip()
    quotes["author"] = quotes["author"].str.strip()
    quotes["tags"] = quotes["tags"].str.strip()
    quotes.insert(0, "id", range(1, len(quotes)+1))
    quotes_file = os.path.join(OUTPUT_DIR, "quotes_clean.csv")
    quotes.to_csv(quotes_file, index=False, encoding="utf-8")
    minio_client.fput_object(bucket_name, "quotes_clean.csv", quotes_file)
    print("Quotes transformés OK")

    # Partenaires
    partners = pd.read_csv(PARTENAIRE_GEO_CSV)
    partners["nom_librairie"] = partners["nom_librairie"].str.strip()
    partners["ville"] = partners["ville"].str.strip()
    partners["specialite"] = partners["specialite"].str.strip()
    for col in ["longitude", "latitude"]:
        if col not in partners.columns:
            partners[col] = None
    cols = ["nom_librairie", "adresse", "code_postal", "ville", "date_partenariat", "specialite", "longitude", "latitude"]
    partners = partners[cols]
    partners.insert(0, "id", range(1, len(partners)+1))
    partners_file = os.path.join(OUTPUT_DIR, "partenaire_clean.csv")
    partners.to_csv(partners_file, index=False, encoding="utf-8")
    minio_client.fput_object(bucket_name, "partenaire_clean.csv", partners_file)
    print("Partenaires transformés OK")
