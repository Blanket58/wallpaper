import requests

from ..util import logger_factory, retry


class Extractor:

    @property
    def logger(self):
        return logger_factory(self.__class__)

    @retry
    def get(self, url):
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
        }
        try:
            self.logger.info(f'GET {url}')
            result = requests.get(url=url, headers=header)
            self.logger.info('OK')
            return result
        except Exception as e:
            self.logger.exception(e)
            raise e

    def today(self):
        pass

    def specify(self, day):
        pass

    def random(self):
        pass
