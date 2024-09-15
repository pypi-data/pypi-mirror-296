import sys
from wordman.core.database import init_db
from wordman.core.word_operations import insert_word, import_list, sort_list

def add_command(args):
    if len(args) < 1:
        print("Usage: wordman add <word>")
        return
    word = args[0]
    insert_word(word, "default")

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