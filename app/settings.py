import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(BASE_DIR, 'media')
SEARCH_SITE = 'https://muzfan.net/?do=search&subaction=search&story={}'
DATE = str(int(datetime.timestamp(datetime.now())))
DATE_FOLDER = os.path.join(MEDIA, DATE)
JSON = os.path.join(MEDIA, 'json')
AUDIO = os.path.join(DATE_FOLDER, 'audio')
IMAGE = os.path.join(DATE_FOLDER, 'image')
OTHER = os.path.join(DATE_FOLDER, 'other')


if not os.path.exists(MEDIA):
    os.makedirs(MEDIA)
if not os.path.exists(JSON):
    os.makedirs(JSON)


def json_name(file):
    if not file:
        file = 'content{}-{}.json'
    elif file.find('.json') == -1:
        file += '{}-{}.json'
    else:
        index = file.rfind('.')
        file = file[0:index] + '{}-{}' + file[index + 1:-1]
    return os.path.join(JSON, file)
