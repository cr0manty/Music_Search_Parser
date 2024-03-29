from mongoengine import connect
import urllib.request
import shutil

from app.models import Artist, Song, Log
from app.settings import *


class MusicSearchDB:
    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        connect('music_search', host=self.host, port=self.port)

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
            Log(
                type_added='artist',
                name_added=artist_name
            ).save()
            return False

        self.download(kwargs.get('img'))
        artist = Artist(name=artist_name)

        if artist:
            Log(
                type_added='artist',
                name_added=artist_name,
                added=True
            ).save()
            with open(TEMP_FILE, 'rb') as binary_file:
                artist.image.put(binary_file)
            shutil.rmtree(TEMP)

            artist.save()
            return True
        Log(
            type_added='artist',
            name_added=artist_name
        ).save()
        return False

    def add_song(self, **kwargs):
        artist_name = kwargs.get('title')[0]
        artist = Artist.objects(name=artist_name)

        song_name = kwargs.get('title')[-1]
        if not artist or Song.objects(name=song_name):
            self.add_artist(**kwargs)

        if self.is_song_exist(song_name):
            Log(
                type_added='song',
                name_added=song_name
            ).save()
            return False

        self.download(kwargs.get('download_url'))
        size = kwargs.get('duration_size')
        size = ' '.join((size[2], size[3]))
        song = Song(artist=artist.get(), name=song_name,
                    duration=kwargs.get('duration_size')[0],
                    download_url=kwargs.get('download_url'),
                    size=size
                    )
        with open(TEMP_FILE, 'rb') as binary_file:
            song.audio_file.put(binary_file)
        shutil.rmtree(TEMP)
        if song:
            song.save()
            Log(
                type_added='song',
                name_added=song_name,
                added=True
            ).save()
            return True

        Log(
            type_added='song',
            name_added=song_name
        ).save()
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
    def to_json_artist(media=False):
        artists = Artist.objects()
        if not artists:
            return False
        return artists.to_json(indent=4, ensure_ascii=False, media=media)

    @staticmethod
    def to_json_song(media=False):
        song = Song.objects()
        if not song:
            return False
        return song.to_json(indent=4, ensure_ascii=False, media=media)
