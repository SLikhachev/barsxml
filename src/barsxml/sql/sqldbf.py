
import pyodbc
from barsxml.config.xmltype import TYPES
from barsxml.sql.sqlbase import SqlBase


# DBF Sql PROVIDER
class SqlProvider(SqlBase):
    
    def __init__(self, config, mo_code, year, month):
        super().__init__(config, mo_code, year, month)
        self.mo = mo_code[:3]
        self.dbfn = f'{self.mo}{self.ye_ar[1]}{self.month}'
        self.dbf_connect()
        self.usl = {}

    def dbf_connect(self):
        self.db_dir = self.config.RR_DIR
        print("DBF dir ", self.db_dir)
        conns = "Driver={Microsoft dBASE Driver (*.dbf)};DefaultDir=%s" % self.db_dir
        self.db = pyodbc.connect(conns, autocommit=True)
        self.rr = f'RR{self.dbfn}.dbf'
        self.rp = f'RP{self.dbfn}.dbf'
        self.rs = f'RS{self.dbfn}.dbf'
        self.curs = self.db.cursor()
        return self

    def truncate_errors(self):
        pass
    
    def get_hpm_data(self, type, get_fresh):
        get_rrs = self.config.GET_RRS % (self.rr, TYPES[type])
        return self.curs.execute(get_rrs).fetchall()

    def get_npr_mo(self, data):
        return getattr(data, 'npr_mo', None)
            
    def get_usl(self, data):
        get_rps = self.config.GET_RPS % self.rp
        return self.curs.execute(get_rps, (data.idcase,)).fetchall()

    def get_all_usl(self):
        get_rps = self.config.GET_ALL_RPS % self.rp
        # curs = self.db.cursor()
        for rps in self.curs.execute(get_rps).fetchall():
            if self.usl.get(rps.nusl, None) is None:
                self.usl[rps.nusl] = [rps]
                continue
            self.usl[rps.nusl].append(rps)

    def get_all_usp(self):
        return None

    def get_pmu_usl(self, idcase):
        return self.usl.get(idcase, [])

    def get_spec_usl(self, data):
        return None
    
    def set_error(self, idcase, card, error):
        pass
    
    def mark_as_sent(self, data):
        pass

    def close(self):
        self.curs.close()
        self.db.close()