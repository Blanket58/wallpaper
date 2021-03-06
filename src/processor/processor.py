import requests

from ..db import DataBase
from ..util import logger_factory, md5, change_wallpaper


class Processor:

    def __init__(self, extractor):
        self.extractor = extractor
        self.logger.info('Using extractor -> ' + extractor.__name__)

    @property
    def logger(self):
        return logger_factory(self.__class__)

    def persistent(self, data):
        try:
            header = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
            }
            self.logger.info(f'Downloading {data.get("url")}')
            response = requests.get(url=data.get('url'), headers=header)
            self.logger.info('OK')
            file_hash = md5(response.content)
            with DataBase() as db:
                db.set(file_hash, data)
            self.logger.info('Hash check pass')
            with open(data.get('location'), 'wb') as f:
                f.write(response.content)
            self.logger.info(f'File saved at {data.get("location")}')
            change_wallpaper(data.get('location'))
        except Exception as e:
            self.logger.exception(e)

    def process(self, *args):
        pass
