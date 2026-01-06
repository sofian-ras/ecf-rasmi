# conformité rgpd

ce document explique comment nous avons traité les données personnelles dans le projet pour respecter le rgpd.

## 1. identification des données personnelles

dans nos sources, nous avons identifié les données personnelles suivantes :  

- **nom du contact** des librairies  
- **email du contact**  
- **téléphone du contact**  

ces informations proviennent du fichier partenaire `partenaire_librairies.xlsx`.

toutes les autres données sont publiques (nom librairie, adresse, code postal, ville, chiffre d’affaires, spécialité).

---

## 2. mesures de protection

pour protéger les données personnelles, nous avons appliqué :  

- **anonymisation** :  
  - remplacement des noms et emails par des identifiants ou pseudonymes  
- **suppression** :  
  - les numéros de téléphone ont été supprimés  
- **stockage sécurisé** :  
  - les données anonymisées sont stockées dans des fichiers csv et dans la base postgresql  
- **contrôle d’accès** :  
  - seules les personnes autorisées peuvent accéder aux données  

---

## 3. base légale du traitement

- le traitement est nécessaire pour la **gestion des partenariats** et pour **réaliser des analyses statistiques**  
- nous ne partageons pas les données personnelles en dehors du projet  
- tout traitement est limité aux informations strictement nécessaires  

---

## 4. droit à l’effacement

- si un contact souhaite que ses données soient supprimées :  
  - nous supprimons manuellement ou automatiquement son enregistrement du fichier csv et de la base postgresql  
- cette procédure permet de respecter le **droit à l’effacement** selon le rgpd  

---

## 5. conclusion

nous avons vérifié que :  
- toutes les données personnelles sont protégées  
- seules les données anonymisées sont utilisées pour l’analyse  
- le projet respecte les exigences légales du rgpd
