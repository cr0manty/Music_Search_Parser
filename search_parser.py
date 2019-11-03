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
        context = {}
        title = element.find('h2', class_='playlist-name')
        download = element.find('a', class_='playlist-btn-down')
        if not title or not download:
            return None

        title = title.find_all('a')
        context['artist'] = {
            'name': title[0].text,
            'artist_link': self.main_url + title[0].get('href')
        }

        context['song'] = {
            'name': title[1].text,
            'song_link': self.main_url + title[1].get('href'),
            'duration': element.find('span', class_='playlist-duration').text,
            'download': self.main_url + download.get('href')
        }
        return context

    def __len__(self):
        return len(self.content)

    def to_json(self):
        return json.dumps(self.content, sort_keys=True, indent=4)

    def write_json(self):
        with open('content.json', 'w') as file:
            json.dump(self.content, file, sort_keys=True, indent=4)

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
        except Exception as e:
            print(e)
            print('Invalid json!')

    def update_content(self, content):
        self.check_content(content)
        self.content[len(self)] = content

    @staticmethod
    def check_content(content):
        if not content['artist'] or not content['song']:
            raise ValueError
        elif not content['artist']['name'] or not content['artist']['artist_link']:
            raise ValueError
        elif not content['song']['name'] or not content['song']['song_link'] \
                or not content['song']['duration'] or not content['song']['download']:
            raise ValueError
