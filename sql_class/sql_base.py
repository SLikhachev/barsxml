
import importlib
from abc import ABC, abstractmethod


def get_sql_provider(config):
    return importlib.import_module(f'barsxml.sql_class.sql_{config.SQL}')


class SqlBase(ABC):
    
    def __init__(self, config, year, month):
        self.config = config
        self.year = year
        self.month = month
        self.ye_ar = year[2:] # last 2 digits as str
        self.truncate_errors()

    @abstractmethod
    def truncate_errors(self):
        pass

    @abstractmethod
    def get_hpm_data(self, get_fresh):
        pass

    @abstractmethod
    def get_ksg_data(self, get_fresh):
        pass

    @abstractmethod
    def get_npr_mo(self, data):
        pass

    @abstractmethod
    def get_usl(self, data):
        pass

    @abstractmethod
    def get_spec_usl(self, data):
        pass

    @abstractmethod
    def set_error(self, data, error):
        pass

    @abstractmethod
    def mark_as_sent(self, data):
        pass

    def check_covid(self, data):
        return False

    @abstractmethod
    def close(self):
        pass

