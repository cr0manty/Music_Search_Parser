from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from config import check_artist_content, check_song_content


class DBConnection:
    def __init__(self, host='localhost', port=27017):
        try:
            self.client = MongoClient(host=host, port=port)
            self.data = self.client.music_search
        except ConnectionFailure:
            raise ConnectionFailure("Can't connect to MongoDB '{}:{}'".format(host, port))
        except Exception as e: #delete
            print(e)

    def add_artist(self, artist):
        self.data.artist.insert(artist)

    def add_song(self, content):
        if not self.is_artist_exist(content['artist']):
            raise Exception("Artist doesn't exist")

        self.data.tracklist.insert(content)

    def add_artists(self, artists):
        pass

    def add_tracklist(self, tracklist):
        pass

    def get_artist_tracklist(self, artist_name):
        pass

    def get_artist_by_song(self, song_name):
        pass

    def get_artist(self, artist_name):
        return self.data.artist.find(artist_name)

    def is_artist_exist(self, artist_name):
        return self.data.artist.find(artist_name).count()

    def show_all(self):
        return self.data.artist.find()

    def to_json(self):
        pass

    def __len__(self):
        return self.data.artist.find().count()


