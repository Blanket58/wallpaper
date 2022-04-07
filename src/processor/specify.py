from .processor import Processor


class Specify(Processor):

    def process(self, day):
        self.persistent(self.extractor().specify(day))
