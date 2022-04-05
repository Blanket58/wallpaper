from .processor import Processor
from ..extractor import Bing, IoLiuAPI


class Specify(Processor):

    def __init__(self):
        self.bing = Bing()
        self.ioliu_api = IoLiuAPI()

    def process(self, day):
        self.logger.info('Using extractor -> Bing')
        for i in range(3):
            try:
                return self.persistent(self.bing.specify(day))
            except KeyError:
                return
            except Exception as e:
                self.logger.exception(e)
                self.logger.warning(f'Retrying [{i + 1} / {3}]')
        self.logger.warning('Switch to extractor -> IoLiuAPI')
        for i in range(3):
            try:
                return self.persistent(self.ioliu_api.specify(day))
            except KeyError:
                return
            except Exception as e:
                self.logger.exception(e)
                self.logger.warning(f'Retrying [{i + 1} / {3}]')
        self.logger.exception('Failed')
