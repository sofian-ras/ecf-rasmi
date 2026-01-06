import os
import pandas as pd
from sqlalchemy import create_engine
from settings import OUTPUT_DIR, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT

engine = create_engine(
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
print("Connexion PostgreSQL OK")

def load_all():
    for file, table in [("books_clean.csv", "books"), ("quotes_clean.csv", "quotes"), ("partenaire_clean.csv", "partenaire")]:
        path = os.path.join(OUTPUT_DIR, file)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        df = pd.read_csv(path)
        df.to_sql(table, engine, if_exists="replace", index=False)
        print(f"{table.capitalize()} chargés OK : {len(df)}")
