""" ODBC (DBF) SQL privider implementation """

import pyodbc
from barsxml.config.xmltype import TYPES
from barsxml.sql.sqlbase import SqlBase


# DBF Sql PROVIDER
class SqlProvider(SqlBase):
    """ class """
    def __init__(self, config):
        super().__init__(config)
        self.dbfn = f'{config._mo}{str(config.ye_ar[1])}{config.month}'
        self.dbf_connect()
        self.usl = {}

    def dbf_connect(self):
        """ method """
        self.db_dir = self.cfg.sql.RR_DIR
        print("DBF dir ", self.db_dir)
        conns = "Driver={Microsoft dBASE Driver (*.dbf)};DefaultDir=%s" % self.db_dir
        self._db = pyodbc.connect(conns, autocommit=True)
        self._rr = f'RR{self.dbfn}.dbf'
        self._rp = f'RP{self.dbfn}.dbf'
        self._rs = f'RS{self.dbfn}.dbf'
        self.curs = self._db.cursor()
        return self

    def truncate_errors(self):
        pass

    def get_hpm_data(self, get_fresh):
        get_rrs = self.cfg.sql.GET_RRS % (self._rr, TYPES[self.cfg.pack_type])
        return self.curs.execute(get_rrs).fetchall()

    def get_npr_mo(self, data):
        return getattr(data, 'npr_mo', None)

    def get_usl(self, data):
        """ method """
        get_rps = self.cfg.sql.GET_RPS % self._rp
        return self.curs.execute(get_rps, (data.idcase,)).fetchall()

    def get_all_usl(self):
        """ method """
        get_rps = self.cfg.sql.GET_ALL_RPS % self._rp
        # curs = self.db.cursor()
        for rps in self.curs.execute(get_rps).fetchall():
            if self.usl.get(rps.nusl, None) is None:
                self.usl[rps.nusl] = [rps]
                continue
            self.usl[rps.nusl].append(rps)

    def get_all_usp(self):
        """ method """
        return None

    def get_pmu_usl(self, idcase):
        return self.usl.get(idcase, [])

    def get_spec_usl(self, profil):
        return None

    def set_error(self, idcase, card, error):
        pass

    def mark_as_sent(self, idcase):
        pass

    def close(self):
        self.curs.close()
        self._db.close()
