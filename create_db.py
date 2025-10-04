import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('TTMIK_BI.db')
c = conn.cursor()

# --- TABLES ---

# Table des utilisateurs / apprenants
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    region TEXT,
    joining_date DATE
)
''')

# Table des abonnements
c.execute('''
CREATE TABLE IF NOT EXISTS subscriptions (
    subscription_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    start_date DATE,
    end_date DATE,
    plan_type TEXT,
    renewed INTEGER, -- 1 si renouvelé, 0 sinon
    price REAL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
''')

# Table des cours
c.execute('''
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT,
    level TEXT,
    type TEXT,
    total_lessons INTEGER
)
''')

# Progression des apprenants dans les cours
c.execute('''
CREATE TABLE IF NOT EXISTS user_course_progress (
    progress_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    course_id INTEGER,
    completed_lessons INTEGER,
    last_activity DATE,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
)
''')

# Table des livres
c.execute('''
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    category TEXT,
    format TEXT, -- papier, audio, ebook
    price REAL
)
''')

# Ventes de livres
c.execute('''
CREATE TABLE IF NOT EXISTS book_sales (
    sale_id INTEGER PRIMARY KEY,
    book_id INTEGER,
    sale_date DATE,
    quantity INTEGER,
    total_amount REAL,
    region TEXT,
    FOREIGN KEY(book_id) REFERENCES books(book_id)
)
''')

# Revenus globaux
c.execute('''
CREATE TABLE IF NOT EXISTS revenues (
    revenue_id INTEGER PRIMARY KEY,
    source TEXT, -- 'book_sales', 'subscriptions', 'youtube_memberships'
    amount REAL,
    date DATE
)
''')

# --- DONNÉES FACTICES TTMIK ---

users = [
    (1, 'Seline', 'Amérique du Nord', '2024-01-10'),
    (2, 'Edward', 'Europe', '2024-02-05'),
    (3, 'Kim', 'Asie', '2024-03-12'),
    (4, 'Diana', 'Amérique du Sud', '2024-04-20'),
    (5, 'Moufdi', 'Afrique', '2024-05-01')
]

subscriptions = [
    (1, 1, '2025-01-01', '2025-06-30', 'Annuel', 1, 100),
    (2, 2, '2025-02-01', '2025-07-31', 'Mensuel', 0, 60),
    (3, 3, '2025-03-01', '2025-08-31', 'Mensuel', 1, 10),
    (4, 4, '2025-04-01', '2025-09-30', 'Annuel', 0, 100),
    (5, 5, '2025-05-01', '2025-10-31', 'Mensuel', 1, 10)
]

courses = [
    (1, 'Core Grammar Level 1', 'Débutant', 'Audio', 26),
    (2, 'Core Grammar Level 2', 'Débutant', 'Audio', 25),
    (3, 'Core Grammar Level 3', 'Débutant', 'Audio', 30),
    (4, 'Core Grammar Level 4', 'Intermédiaire', 'Audio', 28),
    (5, 'Core Grammar Level 5', 'Intermédiaire', 'Audio', 27),
    (6, 'Core Grammar Level 6', 'Intermédiaire', 'Audio', 29),
    (7, 'Core Grammar Level 7', 'Avancé', 'Audio', 26),
    (8, 'Core Grammar Level 8', 'Avancé', 'Audio', 24),
    (9, 'Core Grammar Level 9', 'Avancé', 'Audio', 25),
    (10, 'Core Grammar Level 10', 'Avancé', 'Audio', 30),
    (11, 'Learn to Read and Write in Korean (Hangeul)', 'Débutant', 'Audio & Text', 7),
    (12, 'IYAGI – Listening in 100% Natural Korean', 'Intermédiaire', 'Audio', 145),
    (13, 'The Korean Jigsaw Puzzle: Hanja', 'Intermédiaire', 'Audio', 10),
    (14, 'Korean Idiomatic Expressions [Intermediate]', 'Intermédiaire', 'Audio', 10),
    (15, 'Cultural Topics with Andreas the Greek', 'Avancé', 'Audio', 30),
    (16, 'Korean Buzzwords', 'Intermédiaire', 'Audio', 16),
    (17, 'Beginner’s Guide to Living in Korea', 'Tous niveaux', 'Audio', 10),
    (18, 'Common Mistakes Korean Learners Make (And How To Fix Them) with Go! Billy Korean', 'Tous niveaux', 'Audio', 50)
]

user_course_progress = [
    (1, 1, 1, 18, '2025-05-01'),
    (2, 2, 2, 10, '2025-06-10'),
    (3, 3, 3, 25, '2025-07-15'),
    (4, 4, 1, 12, '2025-08-20'),
    (5, 5, 2, 5, '2025-09-25')
]

books = [
    (1, 'Talk To Me In Korean Textbook Level 1', 'Grammar / Core Course', 'papier / eBook', 17.99),
    (2, 'Korean Folktales in Everyday Conversation', 'Reading / Stories', 'eBook / Paper', 23.99),
    (3, '10-minute Korean: Daily Conversation Practice For Beginners', 'Conversation / Speaking', 'eBook / Paper', 19.99),
    (4, 'Your First Hanja Guide', 'Hanja / Characters', 'eBook / Paper', 27.99),
    (5, 'Korean Phrasebook For Travelers', 'Travel Phrases', 'eBook / Paper', 21.99),
    (6, 'Korean Slang Expressions', 'Slang / Informal', 'eBook / Paper', 19.99),
    (7, 'Common Mistakes Korean Learners Make', 'Usage / Error', 'eBook / Paper', 22.99),
    (8, 'Korean Cultural Expressions', 'Culture / Expressions', 'eBook / Paper', 63.62)
]


book_sales = [
    (1, 1, '2025-01-10', 2, 50, 'Europe'),
    (2, 2, '2025-02-15', 3, 45, 'Asie'),
    (3, 3, '2025-03-20', 1, 20, 'Amérique du Nord'),
    (6, 4, '2025-06-02', 2, 56, 'Océanie'),
    (7, 5, '2025-06-18', 1, 22, 'Amérique du Sud'),
    (8, 6, '2025-07-10', 3, 60, 'Amérique du Nord'),
    (9, 7, '2025-07-30', 2, 46, 'Asie'),
    (10, 8, '2025-08-05', 1, 64, 'Europe'),
    (11, 3, '2025-08-25', 5, 100, 'Amérique du Nord'),
    (12, 5, '2025-09-12', 2, 44, 'Afrique'),
    (13, 6, '2025-09-20', 4, 80, 'Europe'),
    (14, 7, '2025-10-01', 3, 69, 'Asie'),
    (15, 1, '2025-10-15', 2, 50, 'Amérique du Nord'),
    (16, 8, '2025-10-28', 1, 63, 'Océanie'),
    (20, 7, '2025-12-10', 2, 46, 'Amérique du Nord')
]


revenues = [
    (1, 'book_sales', 200, '2025-05-25'),
    (2, 'subscriptions', 280, '2025-05-25'),
    (3, 'youtube_memberships', 90, '2025-05-25')
]

# --- INSERTIONS ---
c.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users)
c.executemany('INSERT INTO subscriptions VALUES (?, ?, ?, ?, ?, ?, ?)', subscriptions)
c.executemany('INSERT INTO courses VALUES (?, ?, ?, ?, ?)', courses)
c.executemany('INSERT INTO user_course_progress VALUES (?, ?, ?, ?, ?)', user_course_progress)
c.executemany('INSERT INTO books VALUES (?, ?, ?, ?, ?)', books)
c.executemany('INSERT INTO book_sales VALUES (?, ?, ?, ?, ?, ?)', book_sales)
c.executemany('INSERT INTO revenues VALUES (?, ?, ?, ?)', revenues)

# Validation et fermeture
conn.commit()
conn.close()

print("✅ Base de données 'TTMIK_BI.db' créée avec succès avec les données adaptées aux KPIs !")
