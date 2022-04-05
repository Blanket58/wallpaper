from .processor import Processor
from ..extractor import Bing, IoLiuAPI


class Random(Processor):

    def __init__(self):
        self.bing = Bing()
        self.ioliu_api = IoLiuAPI()

    def process(self):
        self.logger.info('Using extractor -> IoLiuAPI')
        for i in range(3):
            try:
                return self.persistent(self.ioliu_api.random())
            except KeyError:
                return
            except Exception as e:
                self.logger.exception(e)
                self.logger.warning(f'Retrying [{i + 1} / {3}]')
        self.logger.warning('Switch to extractor -> Bing')
        for i in range(3):
            try:
                return self.persistent(self.bing.random())
            except KeyError:
                return
            except Exception as e:
                self.logger.exception(e)
                self.logger.warning(f'Retrying [{i + 1} / {3}]')
        self.logger.exception('Failed')
