from bs4 import BeautifulSoup
import requests
import json


class SearchEngine:
    content = {}

    def __init__(self):
        self.main_url = 'https://ru-music.com'
        self.search_url = 'https://ru-music.com/search/{}'

    def start(self, for_search):
        html = requests.get(self.search_url.format(for_search)).text
        soup = BeautifulSoup(html, features='html.parser')
        all_tracks = soup.find_all('li', class_='track')

        if all_tracks is None:
            raise Exception('Empty track list')

        self._try_get_list(all_tracks)

    def _try_get_list(self, track_list):
        for i in track_list:
            self._get_artist_info(i)

        return self.content

    async def _get_artist_info(self, element):
        title = element.find('h2', class_='playlist-name')
        download = element.find('a', class_='playlist-btn-down')
        if not title or not download:
            return None

        title = title.find_all('a')

        artist_id = self.check_artist(title[0].text)
        if not artist_id:
            artist_id = len(self)
            self.content[artist_id] = {
                'artist': {
                    'name': title[0].text,
                    'artist_link': self.main_url + title[0].get('href'),
                    'songs': {}
                }
            }

        index = len(self.content[artist_id]['artist']['songs'])
        self.content[artist_id]['artist']['songs'][index] = {
            'name': title[1].text,
            'duration': element.find('span', class_='playlist-duration').text,
            'download': self.main_url + download.get('href')
        }

    def __len__(self):
        length = 0
        for item, value in self.content.items():
            length += len(value['artist']['songs'])
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
                new_content = json.loads(file, ensure_ascii=False)

                if force:
                    for index, value in new_content.items():
                        self._check_content(value)
                    self.content = value
                else:
                    for index, value in new_content.items():
                        self._update_content(value)
        except:
            print('Invalid json!')

    def _update_content(self, content):
        self._check_content(content)
        self.content[len(self)] = content

    def check_artist(self, artist):
        for index, value in self.content.items():
            if value['artist']['name'].lower() == artist.lower():
                return index
        return None

    @staticmethod
    def _check_content(content):
        if not content['artist'] or not content['song']:
            raise ValueError
        elif not content['artist']['name'] or not content['artist']['artist_link']:
            raise ValueError
        elif not content['song']['name'] or not content['song']['song_link'] \
                or not content['song']['duration'] or not content['song']['download']:
            raise ValueError
