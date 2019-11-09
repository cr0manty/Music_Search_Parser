from app.search_parser import SearchEngine

menu = '''
Enter a number to get started:
1 - Start search
2 - Import json
3 - Export json
4 - Print json
5 - Show number of results found
0 - Exit
'''

if __name__ == '__main__':
    search = True
    se = SearchEngine()
    while search:
        result = input(menu)
        if result == '1':
            for_search = input('Enter search query\n')
            if not for_search:
                print("Search query can`t be empty")
            else:
                se.start(for_search)
        elif result == '2':
            file_name = input('Enter file name for export\n')
            se.write_json(file_name)
        elif result == '3':
            print(se.to_json())
        elif result == '4':
            print(len(se))
        elif result == '0':
            search = False
        else:
            print('Wrong input')
