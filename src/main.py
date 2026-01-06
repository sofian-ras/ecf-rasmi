from extract import extract_all
from transform import transform_all
from load_postgres import load_all
from logger import logger

if __name__ == "__main__":
    logger.info("=== PIPELINE START ===")

    extract_all()
    transform_all()
    load_all()

    logger.info("=== PIPELINE END ===")
