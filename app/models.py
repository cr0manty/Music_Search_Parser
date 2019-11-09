from bson import json_util
from datetime import datetime

from mongoengine import Document, QuerySet
from mongoengine import ReferenceField
from mongoengine import StringField, URLField, DateTimeField


class CustomQuerySet(QuerySet):
    def to_json(self, *args, **kwargs):
        return "[%s]" % (",".join([doc.to_json(*args, **kwargs) for doc in self]))


class Artist(Document):
    name = StringField(required=True, unique=True, max_length=100)
    link = URLField(required=True, max_length=256)
    created_at = DateTimeField(default=datetime.now())

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo()
        data['created_at'] = data['created_at'].strftime("%m/%d/%Y, %H:%M:%S")
        return json_util.dumps(data, *args, **kwargs)


class Song(Document):
    artist = ReferenceField(Artist)
    name = StringField(required=True, unique=True, max_length=200)
    duration = StringField(required=True)
    download_url = URLField(required=True)
    created_at = DateTimeField(default=datetime.now())

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo()
        data['artist'] = {'name': self.artist.name}
        data['created_at'] = data['created_at'].strftime("%m/%d/%Y, %H:%M:%S")
        return json_util.dumps(data, *args, **kwargs)
