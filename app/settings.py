import os
from datetime import datetime

SEARCH_SITE = 'https://muzfan.net/?do=search&subaction=search&story={}'
DATE = str(int(datetime.timestamp(datetime.now())))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(BASE_DIR, 'media')
DATE_FOLDER = os.path.join(MEDIA, DATE)
AUDIO = os.path.join(DATE_FOLDER, 'audio')
IMAGE = os.path.join(DATE_FOLDER, 'image')
TEMP = os.path.join(BASE_DIR, 'temp')
TEMP_FILE = os.path.join(TEMP, 'temp.bin')

if not os.path.exists(MEDIA):
    os.makedirs(MEDIA)


def create_folders():
    os.makedirs(DATE_FOLDER)
    os.makedirs(IMAGE)
    os.makedirs(AUDIO)


def json_name(file):
    if not file:
        file = 'content{}-{}.json'
    elif file.find('.json') == -1:
        file += '{}-{}.json'
    else:
        index = file.rfind('.')
        file = file[0:index] + '{}-{}' + file[index + 1:-1]
    return os.path.join(DATE_FOLDER, file)
