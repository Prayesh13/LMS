import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('lms_portal.db')
cursor = conn.cursor()

# Create subjects table
cursor.execute('''
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch TEXT NOT NULL,
    semester INTEGER NOT NULL,
    name TEXT NOT NULL,
    resources TEXT NOT NULL
)
''')

# Insert initial data
subjects_data = [
    ('cse', 1, 'Mathematics I', 'https://maths-resources.com'),
    ('cse', 1, 'Programming in C', 'https://c-programming.com'),
    ('cse', 2, 'Data Structures', 'https://ds-resources.com'),
    ('cse', 2, 'OOP in JAVA', 'https://digital-logic.com'),
    ('ece', 1, 'Engineering Physics', 'https://physics-resources.com'),
    ('ece', 1, 'Basic Electronics', 'https://electronics-basics.com')
]

cursor.executemany("INSERT INTO subjects (branch, semester, name, resources) VALUES (?, ?, ?, ?)", subjects_data)

# Commit and close connection
conn.commit()
conn.close()

print("Database initialized successfully.")
