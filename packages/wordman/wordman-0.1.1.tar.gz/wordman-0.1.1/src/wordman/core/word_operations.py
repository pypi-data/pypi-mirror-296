import os
import bisect
from .database import get_connection

def insert_word(word, list_name=None):
    if list_name is None:
        list_name = "default"

    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT 1 FROM words WHERE word = ?", (word,))
    if c.fetchone():
        print(f"'{word}' already exists in the database.")
        conn.close()
        return

    c.execute("INSERT INTO words (word) VALUES (?)", (word,))
    word_id = c.lastrowid

    c.execute("INSERT OR IGNORE INTO lists (name) VALUES (?)", (list_name,))
    c.execute("SELECT id FROM lists WHERE name = ?", (list_name,))
    list_id = c.fetchone()[0]

    c.execute("INSERT INTO word_list (word_id, list_id) VALUES (?, ?)", (word_id, list_id))

    conn.commit()
    conn.close()

    print(f"'{word}' added to the database and list '{list_name}'.")

    lists_dir = "lists"
    os.makedirs(lists_dir, exist_ok=True)

    txt_file = os.path.join(lists_dir, f"{list_name}.txt")
    dict_file = os.path.join(lists_dir, f"{list_name}.dict")
    
    if os.path.exists(txt_file):
        file_path = txt_file
    elif os.path.exists(dict_file):
        file_path = dict_file
    else:
        file_path = txt_file

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            words = file.read().splitlines()
    else:
        words = []

    if word in words:
        print(f"'{word}' already exists in {file_path}.")
    else:
        bisect.insort(words, word)
        
        with open(file_path, 'w') as file:
            for w in words:
                file.write(w + '\n')
        print(f"'{word}' added to {list_name}")

def import_list(file_path, list_name):
    with open(file_path, 'r') as file:
        words = [word.strip() for word in file]
    
    for word in words:
        insert_word(word, list_name)
    print(f"Imported {len(words)} words into list '{list_name}'")

def sort_list(file_path):
    with open(file_path, 'r') as file:
        words = file.readlines()

    words = [word.strip() for word in words]
    words.sort()

    with open(file_path, 'w') as file:
        for word in words:
            file.write(word + '\n')

def binary_search(file, word):
    low, high = 0, os.path.getsize(file.name)
    while low < high:
        mid = (low + high) // 2
        file.seek(mid)
        file.readline()
        current_pos = file.tell()
        line = file.readline().strip()
        
        if line < word:
            low = current_pos
        else:
            high = mid
            
    return low