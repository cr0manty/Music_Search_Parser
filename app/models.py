from datetime import datetime
from mongoengine import Document
from mongoengine import StringField, URLField, DateTimeField, ReferenceField


class Artist(Document):
    name = StringField(required=True, unique=True, max_length=100)
    link = URLField(required=True, max_length=256)
    created_at = DateTimeField(default=datetime.now())


class Song(Document):
    artist = ReferenceField(Artist)
    name = StringField(required=True, unique=True, max_length=200)
    duration = DateTimeField(required=True)
    download_url = URLField(required=True)
    created_at = DateTimeField(default=datetime.now())

