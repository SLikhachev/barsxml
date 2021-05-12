
import importlib
from abc import ABC, abstractmethod


def get_sql_provider(config):
    return importlib.import_module(f'barsxml.sql.sql{config.SQL}')


class SqlBase(ABC):
    
    def __init__(self, config, year, month):
        self.config = config
        self.year = year
        self.month = month
        self.ye_ar = year[2:] # last 2 digits as str

    @abstractmethod
    def truncate_errors(self):
        pass

    @abstractmethod
    def get_hpm_data(self, type, get_fresh):
        pass

    def get_ksg_data(self, data):
        if getattr(data, 'n_ksg', None) is None:
            return None
        ksg = getattr(self.config, 'KSG', {})
        if len(ksg) == 0:
            raise AttributeError('KSG not provided by Config')
        ksg["n_ksg"] = f"ds{data.n_ksg}"
        ds = getattr(self.config, 'DS', {})
        if len(ds) == 0:
            raise AttributeError('DS not provided by Config')
        ksg["n_ksg"] = f"ds{data.n_ksg}"
        return dict(ds=ds, ksg=ksg)

    @abstractmethod
    def get_npr_mo(self, data):
        pass

    @abstractmethod
    def get_pmu_usl(self, data):
        pass

    @abstractmethod
    def get_spec_usl(self, data):
        pass

    @abstractmethod
    def set_error(self, idcase, card, error):
        pass

    @abstractmethod
    def mark_as_sent(self, data):
        pass

    def check_covid(self, data):
        return False

    @abstractmethod
    def close(self):
        pass

