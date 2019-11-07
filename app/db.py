from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from .config import check_artist_content, check_song_content


class DBConnection:
    def __init__(self, host='localhost', port=27017):
        try:
            self.client = MongoClient(host=host, port=port)
            self.db = self.client.music_search
        except ConnectionFailure:
            raise ConnectionFailure("Can't connect to MongoDB '{}:{}'".format(host, port))

    def add_artist(self, artist):
        check_artist_content(artist)
        self.db.artist.insert(artist)

    def add_song(self, song):
        pass

    def get_artist_songs(self, artist_name):
        pass

    def get_artist_by_song(self, song_name):
        pass

    def __len__(self):
        pass

    def show_all(self):
        pass

    def to_json(self):
        pass
