from .processor import Processor


class Random(Processor):

    def process(self):
        self.persistent(self.extractor().random())
