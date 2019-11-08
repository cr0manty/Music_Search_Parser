from mongoengine import connect

from models import Artist, Song


class DBConnection:
    def __init__(self, host='localhost', port=27017):
        try:
            connect('music_search', host=host, port=port)
        except Exception as e:  # delete
            print(e)

    def add_artist(self, name, link):
        artist = Artist(name=name, link=link)
        if artist:
            artist.save()

    def add_song(self, artist_name, name, duration, download):
        artist = Artist.objects(name=artist_name).get()

        if not artist:
            raise Exception("Artist doesn't exist")

        song = Song(artist=artist, name=name,
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

    def get_artist_tracklist(self, artist_name):
        try:
            song = Song.objects.aggregate(
                {"$lookup": {
                    "from": "song",
                    "foreignField": "_id",
                    "localField": "artist",
                    "as": "artist",
                }},
                {"$unwind": "artist"},
                {"$match": {"artist.name": artist_name}})
            return song
        except Exception:
            print('Error')

    def get_artist_by_song(self, song_name):
        song = Song.objects(name=song_name).get()

        if song:
            return song.artist
        else:
            return None

    def get_artist(self, artist_name):
        return Artist.objects(name=artist_name).get()

    def is_artist_exist(self, artist_name):
        return Artist.objects(name=artist_name).count()

    def show_all_artist(self):
        return Artist.objects()

    def to_json_artist(self):
        return Artist.objects.to_json()

    def to_json_song(self):
        return Song.objects.to_json()

    def from_json(self, json_file):
        pass

    def __len__(self):
        return Artist.objects.count()
