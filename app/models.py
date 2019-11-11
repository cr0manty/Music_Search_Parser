from bson import json_util
from datetime import datetime

from mongoengine import Document, QuerySet
from mongoengine import ReferenceField, FileField, ImageField
from mongoengine import StringField, URLField, DateTimeField


class CustomQuerySet(QuerySet):
    def to_json(self, *args, **kwargs):
        return "[%s]" % (",".join([doc.to_json(*args, **kwargs) for doc in self]))


class Artist(Document):
    name = StringField(required=True, unique=True, max_length=100)
    image = ImageField(required=False)
    created_at = DateTimeField(default=datetime.now())

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo()
        data['created_at'] = data['created_at'].strftime("%m/%d/%Y, %H:%M:%S")
        data.pop('image')
        data.pop('_id')
        return json_util.dumps(data, *args, **kwargs)


class Song(Document):
    artist = ReferenceField(Artist)
    name = StringField(required=True, unique=True, max_length=200)
    duration = StringField(required=True)
    size = StringField(required=False, default='0 Mb')
    download_url = URLField(required=True)
    audio_file = FileField(required=False)
    created_at = DateTimeField(default=datetime.now())

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo()
        data['artist'] = self.artist.name
        data['created_at'] = data['created_at'].strftime("%m/%d/%Y, %H:%M:%S")
        data.pop('audio_file')
        data.pop('_id')
        return json_util.dumps(data, *args, **kwargs)
