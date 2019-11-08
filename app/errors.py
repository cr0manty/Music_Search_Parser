class MongoConnectionError(Exception):
    message = "Can't connect to MongoDB"

    def __init__(self):
        super(MongoConnectionError, self).__init__(self.message)


class ArtistDoesntExist(Exception):
    message = "Artist doesn't exist"

    def __init__(self):
        super(ArtistDoesntExist, self).__init__(self.message)


class SongDoesntExist(Exception):
    message = "Song doesn't exist"

    def __init__(self):
        super(SongDoesntExist, self).__init__(self.message)


class ArtistEmptySongList(Exception):
    message = "Artist doesnt have any song"

    def __init__(self):
        super(ArtistEmptySongList, self).__init__(self.message)
