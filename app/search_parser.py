from bs4 import BeautifulSoup
import requests
import json

from app.db import DBConnection
from config import check_artist_content


class SearchEngine:
    content = {}

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

        for track in all_tracks:
            self._get_artist_info(track)

    def _try_get_list(self, track_list):
        for i in track_list:
            self._get_artist_info(i)

    def _get_artist_info(self, element):
        title = element.find('h2', class_='playlist-name')
        download = element.find('a', class_='playlist-btn-down')
        if not title or not download:
            return None

        title = title.find_all('a')
        if self.database.is_artist_exist(title[0].text):
            self.database.add_artist({
                'name': title[0].text,
                'search_link': self.main_url + title[0].get('href'),
            })

        self.database.add_song({
            'artist': title[0].text,
            'name': title[1].text,
            'duration': element.find('span', class_='playlist-duration').text,
            'download': self.main_url + download.get('href')
        })

    def __len__(self):
        length = 0
        for item, value in self.content.items():
            length += len(value['artist']['tracklist'])
        return length

    def to_json(self):
        return json.dumps(self.content, indent=4, ensure_ascii=False)

    def write_json(self, json_file=''):
        if not json_file:
            json_file = 'content.json'
        elif json_file.find('.json') == -1:
            json_file += '.json'

        with open(json_file, 'w', encoding='utf8') as file:
            json_text = json.dumps(self.content, indent=4, ensure_ascii=False)
            file.write(json_text)

    def import_from_json(self, json_file, force=False):
        try:
            with open(json_file, 'r', encoding='utf8') as file:
                new_content = json.loads(file.read())
                if force:
                    for index, value in new_content.items():
                        check_artist_content(value)
                    self.content = value
                else:
                    for index, value in new_content.items():
                        self.update_content(value)
        except Exception:
            print('Invalid json!')

