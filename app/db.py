from mongoengine import connect
from datetime import datetime

from errors import *
from models import Artist, Song


class DBConnection:
    def __init__(self, host='localhost', port=27017):
        try:
            connect('music_search', host=host, port=port)
        # todo
        except:
            raise MongoConnectionError

    @staticmethod
    def add_artist(name, link):
        artist = Artist(name=name, link=link)
        if artist:
            artist.save()

    @staticmethod
    def add_song(artist_name, name, duration, download):
        artist = Artist.objects(name=artist_name)
        if not artist:
            raise ArtistDoesntExist
        song = Song(artist=artist.get(), name=name,
                    duration=duration, download_url=download)
        if song:
            song.save()

    def add_artists(self, artists):
        for artist in artists:
            self.add_artist(artist['name'], artists['search_link'])

    def add_tracklist(self, tracklist):
        for song in tracklist:
            self.add_song(song['artist'], song['name'],
                          song['duration'], song['download'])

    @staticmethod
    def get_artist_tracklist(artist_name):
        artist = Artist.objects(name=artist_name)
        if not artist:
            raise ArtistDoesntExist
        artist_id = artist.get().id
        tracklist = Song.objects(artist=artist_id)
        if not tracklist:
            raise ArtistEmptySongList
        return tracklist

    @staticmethod
    def get_artist_by_song(song_name):
        song = Song.objects(name=song_name)
        if not song:
            raise SongDoesntExist
        artist = Artist.objects(_id=song.get().artist)
        if not artist:
            raise ArtistDoesntExist
        return artist

    @staticmethod
    def get_artist(artist_name):
        artist = Artist.objects(name=artist_name)
        if not artist:
            raise ArtistDoesntExist
        return artist

    @staticmethod
    def is_artist_exist(artist_name):
        return Artist.objects(name=artist_name).count()

    @staticmethod
    def show_all_artist():
        artists = Artist.objects()
        if not artists:
            raise ArtistDoesntExist
        return artists

    @staticmethod
    def to_json_artist():
        artists = Artist.objects()
        if not artists.count():
            raise ArtistDoesntExist
        return artists.to_json(indent=4, ensure_ascii=False)

    @staticmethod
    def to_json_song():
        song = Song.objects()
        if not song.count():
            raise ArtistDoesntExist
        return song.to_json(indent=4, ensure_ascii=False)

    @staticmethod
    def to_json():
        return Artist.objects.aggregate([
            {'$lookup': {'from': 'song', 'localField': 'song.artist.id', 'foreignField': '_id', 'as': 'song_list'}},
            {'$unwind': '$song_list'},
            {'$project': {'name': 1, 'link': 1, 'created_at': 1,
                          'song_list': {'$song_list.name': 1, '$song_list.duration': 1,
                                        '$song_list.download_link': 1, '$song_list.created_at': 1}}}
        ])

    def __len__(self):
        return Artist.objects.count()
