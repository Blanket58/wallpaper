from .processor import Processor


class Today(Processor):

    def process(self):
        self.persistent(self.extractor().today())
