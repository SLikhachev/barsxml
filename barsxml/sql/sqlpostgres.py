
import psycopg2, psycopg2.extras
from barsxml.config.xmltype import TYPES
from barsxml.sql.sqlbase import SqlBase


# Postgres Sql PROVIDER
class SqlProvider(SqlBase):
    
    def __init__(self, config, year, month):
        super().__init__(config, year, month)
        self.mo = self.config.MO_CODE
        self.db = getattr(config, 'db', None)
        if self.db is None and hasattr(self.config, 'DB_CONN'):
            self.db=psycopg2.connect(self.config.DB_CONN)
        else:
            raise AttributeError("DB_CONN not provided by Config")
        
        self.qurs = self.db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        self.qurs1 = self.db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        self.usl = {}
        self.spec_usl = {}
        self.mo_local={}
        self.get_local_mo()
        self.truncate_errors()
        self.talon_tbl = f'talonz_clin_{self.ye_ar}'
        self.para_tbl = f'para_clin_{self.ye_ar}'
        
    def truncate_errors(self):
        self.qurs1.execute(self.config.TRUNCATE_ERRORS)
        self.db.commit()

    def get_local_mo(self):
        self.qurs1.execute(self.config.GET_ALL_LOCAL_MO)
        for mo in self.qurs1.fetchall():
            self.mo_local[mo.scode] = mo.code

    def get_hpm_data(self, type, get_fresh):
        self.qurs.execute(
            self.config.GET_HPM_DATA,
            (self.talon_tbl, int(self.month), get_fresh))
        return self.qurs.fetchall()

    def get_npr_mo(self, data):
        if hasattr(data, 'from_firm'):
            return self.mo_local.get(data.from_firm, None)
        return None
    
    def get_all_usl(self):
        self.qurs1.execute(self.config.GET_ALL_USL, (
            self.talon_tbl, self.para_tbl, int(self.month)))
        for usl in self.qurs1.fetchall():
            if self.usl.get(usl.idcase, None) is None:
                self.usl[usl.idcase] = [usl]
                continue
            self.usl[usl.idcase].append(usl)

    def get_pmu_usl(self, idcase):
        return self.usl.get(idcase, [])

    def get_all_usp(self):
        self.qurs1.execute(self.config.GET_SPEC_USL)
        for usl in self.qurs1.fetchall():
            self.spec_usl[usl.profil] = usl
    
    def get_spec_usl(self, data):
        return self.spec_usl.get(data.profil, ())
        
    def set_error(self, idcase, card, error):
        self.qurs1.execute(self.config.SET_ERROR, (idcase, card, error))
            
    def mark_as_sent(self, data):
        #UPDATE talonz_clin_%s SET talon_type=2 WHERE tal_num=%s
        query = self.config.MARK_AS_SENT % (self.ye_ar, data.idcase)
        self.qurs1.execute(query)
        
    def close(self):
        self.qurs.close()
        self.qurs1.close()
        self.db.commit()
        self.db.close()
        