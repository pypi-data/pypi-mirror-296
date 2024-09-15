import sqlite3

def init_db():
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS words
                 (id INTEGER PRIMARY KEY, word TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS lists
                 (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS word_list
                 (word_id INTEGER, list_id INTEGER,
                  FOREIGN KEY(word_id) REFERENCES words(id),
                  FOREIGN KEY(list_id) REFERENCES lists(id),
                  PRIMARY KEY(word_id, list_id))''')
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect('wordman.db')