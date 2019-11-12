import sys
from app.search_parser import SearchEngine

help = '''
Usage: manage.py command [args]

Commands:
help
search, args="search query in quotation marks"
export, args=(1/0) - dump media files or not
'''

if __name__ == '__main__':
    try:
        command = sys.argv[1]
    except IndexError:
        command = 'help'
    se = SearchEngine()

    if command == 'help':
        print(help)
    elif command == 'search':
        try:
            for i in range(2, len(sys.argv)-2):
                se.start(sys.argv[i])
        except IndexError:
            print('Invalid command!')
    elif command == 'export':
        try:
            media = sys.argv[2]
        except IndexError:
            media = 0
        se.write_json(media)
    else:
        print('Invalid command!')
