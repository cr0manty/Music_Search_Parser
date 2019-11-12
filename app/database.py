from mongoengine import connect
import urllib.request
import shutil

from app.models import Artist, Song
from app.settings import *


class DBConnection:
    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        try:
            connect('music_search', host=self.host, port=self.port)
        # todo
        except:
            raise Exception("Can't connect to mongodb")

    def __len__(self):
        return Artist.objects.count()

    def __str__(self):
        return 'Host: {}, Port: {}'.format(self.host, self.port)

    def __repr__(self):
        return '{}:{}'.format(self.host, self.port)

    def add_artists(self, artists):
        added = 0
        for artist in artists:
            if self.add_artist(**artist):
                added += 1
        return added

    def add_tracklist(self, tracklist):
        added = 0
        for song in tracklist:
            if self.add_song(**song):
                added += 1
            return added

    def add_artist(self, **kwargs):
        artist_name = kwargs['title'][0]
        artist = Artist.objects(name=artist_name)
        if artist.count():
            return False

        self.download(kwargs.get('img'))
        artist = Artist(name=artist_name)

        with open(TEMP_FILE, 'rb') as binary_file:
            artist.image.put(binary_file)
        shutil.rmtree(TEMP)

        if artist:
            artist.save()
            return True
        return False

    def add_song(self, **kwargs):
        artist_name = kwargs.get('title')[0]
        artist = Artist.objects(name=artist_name)

        song_name = kwargs.get('title')[-1]
        if not artist or Song.objects(name=song_name):
            self.add_artist(**kwargs)

        if self.is_song_exist(song_name):
            return False

        self.download(kwargs.get('download_url'))
        song = Song(artist=artist.get(), name=song_name,
                    duration=kwargs.get('duration_size')[0],
                    download_url=kwargs.get('download_url'),
                    size=kwargs.get('duration_size')[2]
                    )
        with open(TEMP_FILE, 'rb') as binary_file:
            song.audio_file.put(binary_file)
        shutil.rmtree(TEMP)
        if song:
            song.save()
            return True
        return False

    @staticmethod
    def download(url):
        if not os.path.exists(TEMP):
            os.makedirs(TEMP)
        urllib.request.urlretrieve(url, TEMP_FILE)

    @staticmethod
    def get_artist_tracklist(artist_name):
        artist = Artist.objects(name=artist_name)
        if not artist:
            return False
        artist_id = artist.get().id
        tracklist = Song.objects(artist=artist_id)
        if not tracklist:
            raise False
        return tracklist

    @staticmethod
    def get_artist_by_song(song_name):
        song = Song.objects(name=song_name)
        if not song:
            return False
        artist = Artist.objects(_id=song.get().artist)
        if not artist:
            return False
        return artist

    @staticmethod
    def get_artist(artist_name):
        artist = Artist.objects(name=artist_name)
        if not artist:
            return False
        return artist

    @staticmethod
    def is_artist_exist(artist_name):
        return Artist.objects(name=artist_name).count()

    @staticmethod
    def is_song_exist(song_name):
        return Song.objects(name=song_name).count()

    @staticmethod
    def show_all_artist():
        artists = Artist.objects()
        if not artists:
            return False
        return artists

    @staticmethod
    def to_json_artist():
        artists = Artist.objects()
        if not artists:
            return False
        return artists.to_json(indent=4, ensure_ascii=False)

    @staticmethod
    def to_json_song():
        song = Song.objects()
        if not song:
            return False
        return song.to_json(indent=4, ensure_ascii=False)
