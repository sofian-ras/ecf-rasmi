import logging
import os

# Création du dossier logs si inexistant
os.makedirs("logs", exist_ok=True)

# Configurer le logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("pipeline")
