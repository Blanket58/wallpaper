from os import remove

import pickledb

from .util import logger_factory


class DataBase:

    def __init__(self):
        self.connection = pickledb.load('src/data.db', True, sig=False)

    @property
    def logger(self):
        return logger_factory(self.__class__)

    def set(self, key, value):
        self.logger.info('Adding new picture')
        if self.connection.exists(key):
            self.logger.error('Key already exist')
            raise KeyError
        else:
            self.connection.dcreate(key)
            for k, v in value.items():
                self.connection.dadd(key, (k, v))
            self.logger.info('OK')

    def reset(self):
        self.logger.info('Reseting database')
        try:
            remove('src/data.db')
            self.logger.info('OK')
        except FileNotFoundError:
            self.logger.error('Database is not initialized.')

    def __call__(self, key, value):
        return self.set(key, value)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
