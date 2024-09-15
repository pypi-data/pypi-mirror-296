#!/usr/bin/env python3
import sys
import os
import sqlite3
import bisect

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

def insert_word(word, list_name="default"):
    conn = sqlite3.connect('wordman.db')
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
        print(f"'{word}' added to {file_path} in alphabetical order.")

def import_list(file_path, list_name):
    with open(file_path, 'r') as file:
        words = [word.strip() for word in file]
    
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()
    for word in words:
        insert_word(word, list_name)
    conn.close()
    print(f"Imported {len(words)} words into list '{list_name}'")

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

def sort_list(file_path):
    with open(file_path, 'r') as file:
        words = file.readlines()

    words = [word.strip() for word in words]
    words.sort()

    with open(file_path, 'w') as file:
        for word in words:
            file.write(word + '\n')

def add_command(args):
    if len(args) < 2:
        print("Usage: wordman add <word> [list_name]")
        return
    word = args[0]
    list_name = args[1] if len(args) > 1 else "default"
    insert_word(word, list_name)

def import_command(args):
    if len(args) < 2:
        print('Usage: wordman import <file_path> <list_name>')
        return
    file_path, list_name = args
    import_list(file_path, list_name)

def sort_command(args):
    if len(args) < 1:
        print('Usage: wordman sort <file_path>')
        return
    file_path = args[0]
    sort_list(file_path)

def main():
    init_db()

    if len(sys.argv) < 2:
        print('Usage: wordman <command> [arguments]')
        print('Available commands: add, import, sort')
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        'add': add_command,
        'import': import_command,
        'sort': sort_command
    }

    if command in commands:
        commands[command](args)
    else:
        print(f'Invalid command: {command}')
        print('Available commands: add, import, sort')

if __name__ == "__main__":
    main()