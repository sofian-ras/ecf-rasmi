import os
import requests
import pandas as pd
from settings import OUTPUT_DIR, DATA_DIR
from minio import Minio
from logger import logger
from settings import MINIO_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE

# Connexion MinIO
minio_client = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE
)
bucket_name = "ecf-data"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

def download_images(csv_file, bucket_subfolder="images"):
    """
    Télécharge les images listées dans le CSV et les envoie dans MinIO.
    csv_file : chemin vers le CSV contenant la colonne 'image_url' (optionnel)
    bucket_subfolder : sous-dossier du bucket pour les images
    """

    if not os.path.exists(csv_file):
        logger.warning(f"CSV introuvable : {csv_file}. Pas d'images à télécharger.")
        return

    df = pd.read_csv(csv_file)

    if "image_url" not in df.columns or df["image_url"].isna().all():
        logger.info(f"Aucune image à télécharger pour {os.path.basename(csv_file)}")
        return

    # Ajouter un id si inexistant
    if "id" not in df.columns:
        df.insert(0, "id", range(1, len(df) + 1))

    # Dossier local pour stocker temporairement les images
    IMAGES_DIR = os.path.join(DATA_DIR, bucket_subfolder)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    logger.info(f"-> Téléchargement des images depuis {os.path.basename(csv_file)} ...")

    for _, row in df.iterrows():
        image_url = row.get("image_url")
        if not image_url or pd.isna(image_url):
            continue

        image_name = f"{row['id']}_{os.path.basename(image_url)}"
        image_path = os.path.join(IMAGES_DIR, image_name)

        try:
            r = requests.get(image_url, timeout=10)
            r.raise_for_status()
            with open(image_path, "wb") as f:
                f.write(r.content)

            # Upload dans MinIO
            minio_client.fput_object(bucket_name, f"{bucket_subfolder}/{image_name}", image_path)

        except Exception as e:
            logger.error(f"Erreur téléchargement {image_url} : {e}")

    logger.info(f"-> Images téléchargées et envoyées dans MinIO !")
