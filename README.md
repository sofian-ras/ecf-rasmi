# ecf pipeline de données multi-sources

ce projet est un pipeline de données qui collecte, transforme et charge des données depuis plusieurs sources pour les rendre exploitables.

## structure du projet

```

ecf-rasmi/
├── docker-compose.yml
├── requirements.txt
├── README.md
├── docs/
│   ├── DAT.md
│   └── RGPD_CONFORMITE.md
├── src/
│   └── # code python
├── sql/
│   └── analyses.sql
└── data/
└── partenaire_librairies.xlsx

```

## installation et utilisation

1. cloner le projet  
2. installer les dépendances :  
```

pip install -r requirements.txt

```
3. lancer le pipeline complet :  
```

python src/main.py

```
- le pipeline fait : extraction -> transformation -> chargement  
- possibilité de lancer chaque étape séparément depuis `src/`  

## sources de données

- sites web : books to scrape, quotes to scrape  
- api : api adresse pour géocoder les librairies  
- fichier partenaire : partenaire_librairies.xlsx  

## pipeline

1. extraction : scrap des livres et citations, import du fichier excel, téléchargement des images  
2. transformation : nettoyage, conversion, normalisation, déduplication, enrichissement  
3. chargement : insertion des données dans postgresql  

## analyses

dans `sql/analyses.sql` :  
- agrégation simple  
- jointure entre sources  
- fenêtrage  
- top n  
- analyse croisée  

## bonus réalisés

- téléchargement des images pour les livres  
- logging simple pour suivre le pipeline  
- documentation développeur claire  