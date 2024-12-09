import sqlite3

# connecting to the sqlite db
conn = sqlite3.connect('subtrends.db')

# creating a cursor object to execute sql commands
cursor = conn.cursor()


# Create a table for storing Reddit post data
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY, 
    title TEXT NOT NULL,
    score INTEGER,
    num_comments INTEGER,
    created_at TEXT
)
''')

conn.commit()
conn.close()

print("Database and table created successfully!")