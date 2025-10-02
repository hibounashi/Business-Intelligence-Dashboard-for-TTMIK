import sqlite3

# Connexion à la base (ou création si elle n'existe pas)
conn = sqlite3.connect('ventes.db')
c = conn.cursor()

# Création des tables
c.execute('''
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    nom TEXT,
    region TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS produits (
    id INTEGER PRIMARY KEY,
    nom TEXT,
    prix REAL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS ventes (
    id INTEGER PRIMARY KEY,
    client_id INTEGER,
    produit_id INTEGER,
    quantite INTEGER,
    date TEXT,
    FOREIGN KEY(client_id) REFERENCES clients(id),
    FOREIGN KEY(produit_id) REFERENCES produits(id)
)
''')

# Données fictives pour TTMIK
clients = [
    (1, 'Alice', 'Amérique du Nord'),
    (2, 'Bob', 'Europe'),
    (3, 'Charlie', 'Asie'),
    (4, 'Diana', 'Amérique du Sud'),
    (5, 'Ethan', 'Afrique')
]

produits = [
    (1, 'Cours Débutant TTMIK', 50),
    (2, 'Cours Intermédiaire TTMIK', 70),
    (3, 'Cours Avancé TTMIK', 100),
    (4, 'Livre de Grammaire', 30),
    (5, 'Livre de Vocabulaire', 25)
]

ventes = [
    (1, 1, 1, 1, '2025-01-05'),
    (2, 2, 2, 1, '2025-02-10'),
    (3, 3, 3, 1, '2025-03-15'),
    (4, 4, 4, 2, '2025-04-20'),
    (5, 5, 5, 1, '2025-05-25'),
    (6, 1, 2, 1, '2025-06-05'),
    (7, 2, 3, 1, '2025-07-10'),
    (8, 3, 4, 1, '2025-08-15'),
    (9, 4, 1, 2, '2025-09-20'),
    (10, 5, 2, 1, '2025-10-25')
]

# Insertion des données
c.executemany('INSERT INTO clients VALUES (?, ?, ?)', clients)
c.executemany('INSERT INTO produits VALUES (?, ?, ?)', produits)
c.executemany('INSERT INTO ventes VALUES (?, ?, ?, ?, ?)', ventes)

# Validation et fermeture
conn.commit()
conn.close()

print("Base de données 'ventes.db' créée avec succès avec les données fictives TTMIK !")
