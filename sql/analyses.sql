-- Books
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    price_eur DECIMAL(10,2),
    availability VARCHAR(50),
    rating VARCHAR(20),
    source VARCHAR(50)
);

-- Quotes
CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    text TEXT,
    author VARCHAR(100),
    tags VARCHAR(255),
    author_url VARCHAR(255),
    page_url VARCHAR(255),
    source VARCHAR(50)
);

-- Partenaire
CREATE TABLE IF NOT EXISTS partenaire (
    id SERIAL PRIMARY KEY,
    nom_librairie VARCHAR(255),
    adresse VARCHAR(255),
    code_postal VARCHAR(10),
    ville VARCHAR(50),
    date_partenariat DATE,
    specialite VARCHAR(100),
    longitude DECIMAL(10,6),
    latitude DECIMAL(10,6)
);

-- 2. Requêtes

-- 2.1 Agrégation simple : prix moyen des livres
SELECT ROUND(AVG(price_eur), 2) AS prix_moyen_eur
FROM books;

-- 2.2 Jointure : nombre de citations par auteur avec ID pour sécuriser la jointure
SELECT q.author, COUNT(q.id) AS nb_citations
FROM quotes q
LEFT JOIN books b ON q.author = b.title
GROUP BY q.author
ORDER BY nb_citations DESC;

-- 2.3 Fenêtre : classement des livres par prix
SELECT id, title, price_eur,
       RANK() OVER (ORDER BY price_eur DESC) AS rank_price
FROM books;

-- 2.4 Top N : 5 librairies avec les plus récents partenariats
SELECT id, nom_librairie, date_partenariat
FROM partenaire
ORDER BY date_partenariat DESC
LIMIT 5;

-- 2.5 Croisement de sources : livres et librairies par ville
-- On imagine un champ "ville" fictif dans books pour croisement
SELECT p.ville, COUNT(DISTINCT b.id) AS nb_livres
FROM partenaire p
LEFT JOIN books b ON b.source = 'books.toscrape.com'
GROUP BY p.ville
ORDER BY nb_livres DESC;
