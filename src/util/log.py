import logging


class GuiStreamHandler(logging.StreamHandler):

    def emit(self, record):
        print(self.format(record))


def logger_factory(name):
    assert hasattr(name, '__name__') or isinstance(name, str), 'Input must be string or has attribute `__name__`.'
    if hasattr(name, '__name__'):
        name = name.__name__.upper()
    else:
        name = name.upper()
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        gsh = GuiStreamHandler()
        gsh.setFormatter(formatter)
        logger.addHandler(gsh)
    return logger
