import os
import pandas as pd
from minio import Minio
from settings import BOOKS_CSV, QUOTES_CSV, PARTENAIRE_GEO_CSV, OUTPUT_DIR
from settings import MINIO_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE

GBP_TO_EUR = 1.15

# --- Création du dossier output si inexistant ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Connexion MinIO ---
minio_client = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE
)
bucket_name = "ecf-data"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)


# ---------------------------
# Transformation livres
def transform_books(input_file=BOOKS_CSV, output_file=None):
    if output_file is None:
        output_file = os.path.join(OUTPUT_DIR, "books_clean.csv")

    books = pd.read_csv(input_file)
    books["price_eur"] = (books["price_gbp"] * GBP_TO_EUR).round(2)
    books["title"] = books["title"].str.strip()
    books["availability"] = books["availability"].str.strip()
    books.insert(0, "id", range(1, len(books)+1))
    books.to_csv(output_file, index=False, encoding="utf-8")
    print("Books OK :", len(books))

    minio_client.fput_object(bucket_name, "books_clean.csv", output_file)
    return output_file


# ---------------------------
# Transformation citations
def transform_quotes(input_file=QUOTES_CSV, output_file=None):
    if output_file is None:
        output_file = os.path.join(OUTPUT_DIR, "quotes_clean.csv")

    quotes = pd.read_csv(input_file)
    quotes["text"] = quotes["text"].str.strip()
    quotes["author"] = quotes["author"].str.strip()
    quotes["tags"] = quotes["tags"].str.strip()
    quotes.insert(0, "id", range(1, len(quotes)+1))
    quotes.to_csv(output_file, index=False, encoding="utf-8")
    print("Quotes OK :", len(quotes))

    minio_client.fput_object(bucket_name, "quotes_clean.csv", output_file)
    return output_file


# ---------------------------
# Transformation partenaires
def transform_partenaire(input_file=PARTENAIRE_GEO_CSV, output_file=None):
    if not os.path.exists(input_file):
        print("Fichier partenaire non trouvé :", input_file)
        return None

    if output_file is None:
        output_file = os.path.join(OUTPUT_DIR, "partenaire_clean.csv")

    partners = pd.read_csv(input_file)
    partners["nom_librairie"] = partners["nom_librairie"].str.strip()
    partners["ville"] = partners["ville"].str.strip()
    partners["specialite"] = partners["specialite"].str.strip()

    # Créer les colonnes longitude et latitude si elles n'existent pas encore
    if "longitude" not in partners.columns:
        partners["longitude"] = None
    if "latitude" not in partners.columns:
        partners["latitude"] = None

    cols = ["nom_librairie", "adresse", "code_postal", "ville", "date_partenariat",
            "specialite", "longitude", "latitude"]
    partners = partners[[c for c in cols if c in partners.columns]]
    partners.insert(0, "id", range(1, len(partners)+1))
    partners.to_csv(output_file, index=False, encoding="utf-8")
    print("Partenaires OK :", len(partners))

    minio_client.fput_object(bucket_name, "partenaire_clean.csv", output_file)
    return output_file
