""" sql base class def """

from abc import ABC, abstractmethod
import barsxml.config as bcfg


class SqlBase(ABC):
    """ abc for RDBM access """

    def __init__(self, config: object):
        """
            @param: config where:
                sql_srv: dict - sql srver to connect definition
                pack_type: str - pack type
                mo_code: str - full MO code e.g. '250747'
                _mo: str - last 3 digit of mo_code
                year: int - year of the report 2022
                ye_ar: int -  last 2 digit of year
                month - month ot report '01'-'12'
                _month: int(month)
                pack_number: int pack number
                ... some other
        """
        self.cfg = config

    @abstractmethod
    def get_hpm_data(self, get_fresh: bool) -> object:
        """ get hpm record from DB
            @param: pack_type - type of the output type as to TYPES config
            @param: get_fresh - select records with fresh flag only
        """

    @staticmethod
    def rec_to_dict(rec: object) -> dict:
        """ convert DB record object to dict """
        # if dict
        if isinstance(rec, dict):
            return rec

        # if Named Tuple
        if hasattr(rec, "_asdict"):
            return rec._asdict()

        # if ODBC driver rec (DBF file)
        if hasattr(rec, "cursor_description"):
            drec = {}
            for idx, desc in enumerate(rec.cursor_description):
                _fd = rec[idx]
                if isinstance(_fd, float):
                    _fd = int(_fd)
                drec[desc[0]] = _fd
            return drec

        # Unknown record type
        raise AttributeError("Тип записи БД не поддерживается")

    @staticmethod
    def get_ksg_data(n_ksg: str = '') -> dict:
        """ emulate KSG dict
            @param: n_ksg - ksg group number for DS
        """
        if len(n_ksg) == 0:
            return {}
        ksg = getattr(bcfg, 'KSG', None)
        if ksg is None:
            raise AttributeError("Нет 'KSG' в кофигурационном файле")
        assert isinstance(ksg, dict), "KSG должен быть словарем"

        _ds = getattr(bcfg, 'DS', None)
        if _ds is None:
            raise AttributeError("Нет 'DS' в конфигурационном файле")
        assert isinstance(_ds, dict), "DS должен быть словарем"

        # set n_ksg for day stac xml node
        ksg["n_ksg"] = f"ds{n_ksg}"
        return {'ds': _ds, 'ksg': ksg}

    @abstractmethod
    def get_npr_mo(self, data: dict) -> int:
        """ return npr_mo number (mo_code) """

    @abstractmethod
    def get_pmu_usl(self, idcase: int) -> dict:
        """ return dict of pmu usl """

    @abstractmethod
    def get_spec_usl(self, profil: int):# -> list:
        """ return list of spec usl (doctor's appointment codes) """

    @abstractmethod
    def set_error(self, idcase: int, card: str, error: str):
        """ set error in DB errors table """

    @abstractmethod
    def mark_as_sent(self, idcase: int):
        """ mark record as sent """

    def check_covid(self):
        """ pass """
        return False

    @abstractmethod
    def truncate_errors(self):
        """ truncate DB errors table """

    @abstractmethod
    def close(self):
        """ close DB connection """
