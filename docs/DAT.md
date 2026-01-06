# dossier d'architecture technique (dat)

## 1. choix d'architecture globale

nous avons choisi une **architecture type data lake**.  

- pourquoi ce choix :  
  - nous devons stocker des données de plusieurs sources différentes : sites web, api et fichiers partenaires  
  - les données brutes peuvent être de formats différents (csv, json, images)  
  - cela permet de garder toutes les données originales et de les transformer ensuite  

- avantages :  
  - flexibilité pour stocker tout type de données  
  - facile d’ajouter de nouvelles sources  
  - possibilité de transformer les données plusieurs fois sans perdre l’original  

- inconvénients :  
  - nécessite un stockage structuré pour les analystes  
  - pas optimisé pour les requêtes SQL très complexes par défaut  

---

## 2. choix des technologies

- **stockage des données brutes** : fichiers csv et minio pour les images  
  - justification : facile à manipuler, durable, permet de stocker les images et fichiers lourds  
  - alternative : base noSQL type mongodb, mais moins simple pour csv et images  

- **données transformées** : postgresql  
  - justification : permet d’organiser les données en tables et de faire des requêtes rapides  
  - alternative : mysql, similaire mais postgresql gère mieux certaines fonctions analytiques  

- **interrogation SQL** : postgresql  
  - justification : langage SQL standard, possibilité de créer index et vues  
  - alternative : sqlite, plus simple mais moins adaptée pour volume important ou multi-utilisateurs  

---

## 3. organisation des données

- dossiers principaux :  
  - `data/` pour les données brutes et transformées  
  - `src/` pour le code  
  - `sql/` pour les requêtes analytiques  

- couches de transformation :  
  1. extraction : collecte des données brutes  
  2. transformation : nettoyage, conversion, enrichissement  
  3. chargement : insertion dans postgresql  

- convention de nommage :  
  - fichiers csv : `books.csv`, `quotes.csv`, `partenaire_librairies_geo.csv`  
  - tables : `books`, `quotes`, `partenaire`  
  - colonnes en minuscules et underscores  

---

## 4. modélisation des données

- modèle final : tables relationnelles simples  

- tables :  
  1. books : id, titre, prix, note, disponibilité, catégorie, source  
  2. quotes : id, texte, auteur, tags, source  
  3. partenaire : id, nom_librairie, adresse, code_postal, ville, ca_annuel, specialite, longitude, latitude  

- justification :  
  - tables séparées pour chaque type de données  
  - clé primaire `id` pour identifier chaque enregistrement  
  - possibilité de faire des jointures simples pour analyser plusieurs sources  

---

## 5. conformité rgpd

- données personnelles identifiées :  
  - nom, email, téléphone du contact des librairies  

- mesures de protection :  
  - anonymisation des noms et emails  
  - suppression des téléphones  
  - stockage sécurisé dans csv et postgresql  

- droit à l’effacement :  
  - suppression manuelle ou automatique des enregistrements contenant des données personnelles sur demande  

---
