from mongoengine import connect

from models import Artist, Song


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
            if self.add_artist(artist['name'], artists['search_link']):
                added += 1
        return added

    def add_tracklist(self, tracklist):
        added = 0
        for song in tracklist:
            if self.add_song(song['artist'], song['name'],
                             song['duration'], song['download']):
                added += 1
            return added

    @staticmethod
    def add_artist(name, link):
        if Artist.objects(name=name):
            return False
        artist = Artist(name=name, link=link)
        if artist:
            artist.save()
            return True
        return False

    @staticmethod
    def add_song(artist_name, name, duration, download):
        artist = Artist.objects(name=artist_name)
        if not artist or Song.objects(name=name):
            return False
        song = Song(artist=artist.get(), name=name,
                    duration=duration, download_url=download)
        if song:
            song.save()
            return True
        return False

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

