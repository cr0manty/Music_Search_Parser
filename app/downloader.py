import uuid
import urllib.request

from app.settings import *


class Download:
    name = None
    image_type = ('jpg', 'jpeg', 'png')
    music_type = ('mp3', 'flac')

    def __init__(self):
        self._generate_name()
        self._create_folders()

    def _create_folders(self):
        os.makedirs(IMAGE)
        os.makedirs(AUDIO)
        os.makedirs(OTHER)

    def _generate_name(self):
        self.name = uuid.uuid4().hex[:16].upper()

    def download(self, url, file_type):
        try:
            if file_type in self.music_type:
                file_folder = 'audio'
            elif file_type in self.image_type:
                file_folder = 'image'
            else:
                file_folder = 'other'

            self._generate_name()
            file_name = '{}\\{}\\{}.{}'.format(
                DATE_FOLDER, file_folder, self.name, file_type
            )
            urllib.request.urlretrieve(url, file_name)
            return file_name
        except Exception:
            return None
