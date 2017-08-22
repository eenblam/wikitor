import sqlite3
import sys

try:
    NAME = sys.argv[1]
except IndexError:
    print("Error: no name provided")
    print("This script creates <name>.db with table <name>.")
    print("Usage: python schema.py <name>")
    sys.exit(1)

s = '''CREATE TABLE {}(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    endpoint text,
    content text,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
    );'''.format(NAME)

conn = sqlite3.connect('{}.db'.format(NAME))
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS {}'.format(NAME))
c.execute(s)
conn.commit()
c.close()
