from bs4 import BeautifulSoup
import requests
import json


class SearchEngine:
    content = {}

    def __init__(self):
        self.main_url = 'https://ru-music.com'
        self.search_url = 'https://ru-music.com/search/{}'

    def start(self, for_search):
        self.get_search_result(for_search)

    def get_search_result(self, search):
        html = requests.get(self.search_url.format(search)).text
        soup = BeautifulSoup(html, features='html.parser')
        all_tracks = soup.find_all('li', class_='track')

        if all_tracks is None:
            raise Exception('Empty track list')

        self.try_get_list(all_tracks)

    def try_get_list(self, track_list):
        for i in track_list:
            context = self.get_artist_info(i)
            if context:
                self.content[len(self)] = context

        return self.content

    def get_artist_info(self, element):
        title = element.find('h2', class_='playlist-name')
        download = element.find('a', class_='playlist-btn-down')
        if not title or not download:
            return None

        title = title.find_all('a')

        context = self.check_artist(title[0].text)
        if not context:
            context = {
                'artist': {
                    'name': title[0].text,
                    'artist_link': self.main_url + title[0].get('href'),
                    'songs': {}
                }
            }

        context['artist']['songs'][len(context['artist']['songs'])] = {
            'name': title[1].text,
            'song_link': self.main_url + title[1].get('href'),
            'duration': element.find('span', class_='playlist-duration').text,
            'download': self.main_url + download.get('href')
        }
        return context

    def __len__(self):
        return len(self.content)

    def to_json(self):
        return json.dumps(self.content, indent=4)

    def write_json(self, json_file):
        if not json_file:
            json_file = 'content.json'
        elif json_file.find('.json') == -1:
            json_file += '.json'

        with open(json_file, 'w') as file:
            json.dump(self.content, file, indent=4)

    def import_from_json(self, json_file, force=False):
        try:
            with open(json_file, 'r') as file:
                json_content = file.read()
                new_content = json.loads(json_content)

                if force:
                    for i in new_content:
                        content = new_content[i]
                        self.check_content(content)
                    self.content = new_content
                else:
                    for i in new_content:
                        content = new_content[str(i)]
                        self.update_content(content)
        except:
            print('Invalid json!')

    def update_content(self, content):
        self.check_content(content)
        self.content[len(self)] = content

    def check_artist(self, artist):
        for i in self.content:
            if self.content[i]['artist']['name'].lower() == artist.lower():
                return self.content[i]

    @staticmethod
    def check_content(content):
        if not content['artist'] or not content['song']:
            raise ValueError
        elif not content['artist']['name'] or not content['artist']['artist_link']:
            raise ValueError
        elif not content['song']['name'] or not content['song']['song_link'] \
                or not content['song']['duration'] or not content['song']['download']:
            raise ValueError
