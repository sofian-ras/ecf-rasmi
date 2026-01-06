import pandas as pd
import csv
from settings import PARTENAIRE_FILE, PARTENAIRE_GEO_CSV, DATA_DIR

def anonymize_row(row):
    """
    Anonymisation simple des données personnelles
    """
    row['contact_nom'] = "ANONYME"
    row['contact_email'] = f"anonyme{row.name}@exemple.com"
    row['contact_telephone'] = None
    return row

def import_excel(input_file=PARTENAIRE_FILE, output_file=PARTENAIRE_GEO_CSV):
    """
    Importe le fichier partenaire et anonymise les données personnelles.
    Sauvegarde un CSV prêt pour le pipeline.
    """
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {input_file} : {e}")
        return

    # Vérification colonnes essentielles
    expected_cols = ['nom_librairie', 'adresse', 'code_postal', 'ville', 
                     'contact_nom', 'contact_email', 'contact_telephone', 
                     'ca_annuel', 'date_partenariat', 'specialite']
    missing = [col for col in expected_cols if col not in df.columns]
    if missing:
        print(f"Colonnes manquantes : {missing}")
        return

    # Anonymisation
    df = df.apply(anonymize_row, axis=1)

    # Sauvegarde CSV
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Fichier CSV anonymisé créé : {output_file}")

if __name__ == "__main__":
    import_excel()
