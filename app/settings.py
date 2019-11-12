import os
from datetime import datetime

SEARCH_SITE = 'https://muzfan.net/?do=search&subaction=search&story={}'
DATE = str(int(datetime.timestamp(datetime.now())))
TIME_FORMAT = '%m/%d/%Y %H:%M:%S'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(BASE_DIR, 'media')
DATE_FOLDER = os.path.join(MEDIA, DATE)
AUDIO = os.path.join(DATE_FOLDER, 'audio')
IMAGE = os.path.join(DATE_FOLDER, 'image')
TEMP = os.path.join(BASE_DIR, 'temp')
TEMP_FILE = os.path.join(TEMP, 'temp.bin')

if not os.path.exists(MEDIA):
    os.makedirs(MEDIA)


def create_folders(media):
    os.makedirs(DATE_FOLDER)
    if media:
        os.makedirs(IMAGE)
        os.makedirs(AUDIO)


def json_name():
    return os.path.join(DATE_FOLDER, 'content{}-{}.json')
