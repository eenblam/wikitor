import sqlite3

s = '''CREATE TABLE pages(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    endpoint text,
    content text,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
    );'''

conn = sqlite3.connect('pages.db')
c = conn.cursor()
c.execute(s)
conn.commit()
c.close()
