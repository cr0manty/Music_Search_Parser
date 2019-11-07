def check_artist_content(content):
    if not content['artist'] or not content['artist']['tracklist'] or \
            not content['artist']['name'] or not content['artist']['search_link']:
        raise TypeError


def check_song_content(content):
    pass
