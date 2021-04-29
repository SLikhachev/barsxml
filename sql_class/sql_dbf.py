
import pyodbc
from barsxml.config.xml_type import TYPES
from barsxml.sql_class.sql_base import SqlBase

# DBF Sql PROVIDER

class SqlProvider(SqlBase):
    
    def __init__(self, config, year, month):
        super().__init__(config, year, month)
        self.mo = self.config.MO_CODE
        self.dbfn = f'{self.mo}{self.ye_ar[1]}{self.month}'
        self.dbf_connect()
        self.usl = {}

    def dbf_connect(self):
        self.db_dir = self.config.RR_DIR
        #print("DBF dir ", self.db_dir)
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
        #curs = self.db.cursor()
        rrs = self.curs.execute(get_rrs).fetchall()
        #curs.close()
        return rrs

    def get_ksg_data(self, data):
        if getattr(data, 'n_ksg', None) is None:
            return None
        ksg = self.config.KSG
        ksg["n_ksg"] = f"ds{data.n_ksg}"
        return dict(ds=self.config.DS, ksg=ksg)

    def get_npr_mo(self, nmo):
        return nmo
            
    def get_usl(self, data):
        get_rps = self.config.GET_RPS % self.rp
        #curs = self.db.cursor()
        rps = self.curs.execute(get_rps, (data.idcase,)).fetchall()
        #curs.close()
        return rps

    def get_all_usl(self):
        get_rps = self.config.GET_ALL_RPS % self.rp
        # curs = self.db.cursor()
        for rps in self.curs.execute(get_rps).fetchall():
            if self.usl.get(rps.nusl, None) is None:
                self.usl[rps.nusl] = [rps]
                continue
            self.usl[rps.nusl].append(rps)
        # curs.close()
        #return rps

    def _get_usl(self, idcase):
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