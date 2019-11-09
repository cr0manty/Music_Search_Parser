from bs4 import BeautifulSoup
from json import loads as json_load

import requests

from app.db import DBConnection


class SearchEngine:
    def __init__(self, host='localhost', port=27017):
        self.main_url = 'https://ru-music.com'
        self.search_url = 'https://ru-music.com/search/{}'
        self.database = DBConnection(host, port)

    def start(self, for_search):
        html = requests.get(self.search_url.format(for_search)).text
        soup = BeautifulSoup(html, features='html.parser')
        all_tracks = soup.find_all('li', class_='track')

        if all_tracks is None:
            raise Exception('Empty track list')

        artist_add, song_add = 0, 0
        for track in all_tracks:
            amount = self._get_artist_info(track)
            artist_add += amount[0]
            song_add += amount[1]
        print('Artist added - {}, Song added - {}'.format(artist_add, song_add))

    def _get_artist_info(self, element):
        title = element.find('h2', class_='playlist-name')
        download = element.find('a', class_='playlist-btn-down')
        if not title or not download:
            return None

        title = title.find_all('a')
        artist_add, song_add = 0, 0
        if not self.database.is_artist_exist(title[0].text):
            if self.database.add_artist(title[0].text, self.main_url + title[0].get('href')):
                artist_add = 1

        if self.database.add_song(title[0].text, title[1].text,
                                  element.find('span', class_='playlist-duration').text,
                                  self.main_url + download.get('href')
                                  ):
            song_add = 1
        return artist_add, song_add

    def __len__(self):
        return len(self.database)

    def to_json(self):
        return self.database.to_json_artist(), \
               self.database.to_json_song()

    def write_json(self, json_file=''):
        if not json_file:
            json_file = 'content{}.json'
        elif json_file.find('.json') == -1:
            json_file += '{}.json'
        else:
            index = json_file.rfind('.')
            json_file = json_file[0:index] + '{}' + json_file[index + 1:-1]

        with open(json_file.format('_artist'), 'w', encoding='utf8') as artist_file:
            artist_file.write(self.database.to_json_artist())
        with open(json_file.format('_song'), 'w', encoding='utf8') as song_file:
            song_file.write(self.database.to_json_song())
