from bs4 import BeautifulSoup
import requests
import json


class SearchEngine:
    search_url = 'https://muzfan.net/?do=search&subaction=search&story={}'
    content = {}

    def start(self, for_search):
        html = requests.get(self.search_url.format('+'.join(for_search.split(' ')))).text
        soup = BeautifulSoup(html, features='html.parser')
        all_tracks = soup.find_all('div', class_='track-item')

        if not all_tracks:
            print('Empty track list')
            return

        for i in all_tracks:
            self._get_artist_info(i)

    def _get_artist_info(self, element):
        content = {
            'title': element.get('data-artist').split(' - '),
            'download_url': element.get('data-track'),
            'img': element.get('data-img'),
            'duration_size': element.get('data-title').split(' '),
        }
        artist_id = self.check_artist(content['title'][0])

        if artist_id == -1:
            artist_id = len(self.content)
            self.content[artist_id] = {
                'artist': {
                    'name': content['title'][0],
                    'image': content['img'],
                    'tracklist': {}
                }
            }

        size = ' '.join((content['duration_size'][2], content['duration_size'][3]))
        index = len(self.content[artist_id]['artist']['tracklist'])
        self.content[artist_id]['artist']['tracklist'][index] = {
            'name': content['title'][-1],
            'duration': content['duration_size'][0],
            'size': size,
            'download': content['download_url']
        }

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
                        self.check_content(value)
                    self.content = value
                else:
                    for index, value in new_content.items():
                        self.update_content(value)
        except Exception:
            print('Invalid json!')

    def update_content(self, content):
        self.check_content(content)
        artist_id = self.check_artist(content['artist']['name'])

        if artist_id == -1:
            artist_id = len(self.content)
            self.content[artist_id] = content['artist']

        index = len(self.content[artist_id]['artist']['tracklist'])
        for item in content['artist']['tracklist']:
            self.content[artist_id]['artist']['tracklist'][index] = item
            index += 1

    def check_artist(self, artist):
        for index, value in self.content.items():
            artist_name = ''.join(value['artist']['name'].lower().split(' '))
            if artist_name == ''.join(artist.lower().split(' ')):
                return index
        return -1

    @staticmethod
    def check_content(content):
        if not content['artist'] or not content['artist']['tracklist'] or \
                not content['artist']['name'] or not content['artist']['search_link']:
            raise TypeError
