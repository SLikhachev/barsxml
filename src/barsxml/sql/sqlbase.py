""" sql base """
from abc import ABC, abstractmethod
import barsxml.config as bcfg

class SqlBase(ABC):
    """ class sql base """
    def __init__(self, config: object, mo_code: str, year: str, month: str):
        self.config = config
        self.mo_code = mo_code  # full code 250747
        self.year = int(year)
        self.month = int(month)
        self.ye_ar = self.year - 2000 # last 2 digits

    @abstractmethod
    def get_hpm_data(self, pack_type: str, get_fresh: bool):# -> object:
        """ get hpm data """

    @staticmethod
    def rec_to_dict(rec: object):# -> dict:
        """ dict """
        if isinstance(rec, dict):
            return rec

        # Named Tuple
        if hasattr(rec, "_asdict"):
            return rec._asdict()

        # ODBC driver rec
        if hasattr(rec, "cursor_description"):
            drec = {}
            for idx, desc in enumerate(rec.cursor_description):
                _fd = rec[idx]
                if isinstance(_fd, float):
                    _fd = int(_fd)
                drec[desc[0]] = _fd
            return drec

        print(f'rec_to_dict={rec}')
        # Unknown record type
        raise AttributeError("Can't transform Record to Dict")

    @staticmethod
    def get_ksg_data(n_ksg: str = ''):# -> dict:
        """ ksg  """
        if len(n_ksg) == 0:
            return {}
        ksg = getattr(bcfg, 'KSG', {})
        if len(ksg) == 0:
            raise AttributeError('KSG not provided by Base Config')
        ksg["n_ksg"] = f"ds{n_ksg}"
        _ds = getattr(bcfg, 'DS', {})
        if len(_ds) == 0:
            raise AttributeError('DS not provided by Config')
        ksg["n_ksg"] = f"ds{n_ksg}"
        return dict(ds=_ds, ksg=ksg)

    @abstractmethod
    def get_npr_mo(self, data: dict):# -> int or None:
        """ npr mo """

    @abstractmethod
    def get_pmu_usl(self, idcase: int):# -> dict:
        """ pmu usl """

    @abstractmethod
    def get_spec_usl(self, profil: int):# -> list:
        """ spec usl """

    @abstractmethod
    def set_error(self, idcase: int, card: str, error: str):
        """ set error """

    @abstractmethod
    def mark_as_sent(self, idcase: int):
        """ mark as sent """

    def check_covid(self, *args):
        return False

    @abstractmethod
    def truncate_errors(self):
        """ truncate """

    @abstractmethod
    def close(self, _rc):
        """ close """
