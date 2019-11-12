import requests
from bs4 import BeautifulSoup

from app.settings import *
from app.database import DBConnection


class SearchEngine:
    def __init__(self, host='localhost', port=27017):
        self.database = DBConnection(host, port)

    def start(self, for_search):
        search = SEARCH_SITE.format('+'.join(for_search.split(' ')))
        html = requests.get(search).text
        soup = BeautifulSoup(html, features='html.parser')
        all_tracks = soup.find_all('div', class_='track-item')
        if not all_tracks or all_tracks is None:
            raise Exception('Empty track list')

        amount = 0
        for track in all_tracks:
            if self._get_artist_info(track):
                amount += 1
        print('Song added - {}'.format(amount))

    def _get_artist_info(self, element):
        content = {
            'title': element.get('data-artist').split(' - '),
            'download_url': element.get('data-track'),
            'img': element.get('data-img'),
            'duration_size': element.get('data-title').split(' '),
        }

        if self.database.add_song(**content):
            return True
        return False

    def __len__(self):
        return len(self.database)

    def to_json(self):
        return self.database.to_json_artist(), \
               self.database.to_json_song()

    def write_json(self, media=False):
        create_folders(media)
        json_file = json_name()
        with open(json_file.format('_artist', DATE), 'w', encoding='utf8') as artist_file:
            artist_file.write(self.database.to_json_artist(media))
        with open(json_file.format('_song', DATE), 'w', encoding='utf8') as song_file:
            song_file.write(self.database.to_json_song(media))
