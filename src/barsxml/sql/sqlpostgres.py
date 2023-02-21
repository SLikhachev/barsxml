""" sql postgresql DB provider class impl """

import psycopg2
import psycopg2.extras
from barsxml.sql.sqlbase import SqlBase
from barsxml.config import postgresxml as pg

# Postgres Sql PROVIDER
class SqlProvider(SqlBase):
    """ class impl """

    def __init__(self, config):
        super().__init__(config) #self.cfg = config
        dbc =  getattr(config, 'sql_srv', {})
        #print(f'{dbc["dbname"]} {dbc["user"]} {dbc["password"]}')
        try:
            self._db = psycopg2.connect(
                port=dbc.get('port', 5432),
                host=dbc.get('host', ''),
                dbname=dbc['dbname'],
                user=dbc['user'],
                password=dbc['password']
            )
        except KeyError as kexc:
            raise AttributeError(f"Ошибка в определении словаря SQL_SRV: {kexc}") from kexc
        except psycopg2.Error as pexc:
            raise EnvironmentError(f"Ошибка соеденения с БД {pexc}") from pexc

        self.qurs = self._db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        self.qurs1 = self._db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

        self.cuser = dbc.get('cuser', None) or dbc['user']
        self.usl = {}
        self.spec_usl = {}
        self.mo_local={}
        self.errors_table = dbc.get('errors_table', pg.ERRORS_TABLE_NAME)
        self.talon_tbl = f'{pg.TALONZ_CLIN}{config.ye_ar}'
        self.para_tbl = f'{pg.PARA_CLIN}{config.ye_ar}'
        self.init_session(dbc)
        self.get_local_mo()

    def init_session(self, dbc: dict):
        """ set schema, role and cuser env if any """
        self.qurs.execute(pg.SET_SCHEMA % dbc.get('schema', 'public'))
        if dbc.get('role', None):
            self.qurs.execute(pg.SET_ROLE % dbc['role'])
        self.qurs.execute(pg.SET_CUSER, (self.cuser,))
        if self.errors_table != 'None':
            #pass
            self.truncate_errors()

    def truncate_errors(self):
        print(self.errors_table)
        self.qurs1.execute(pg.TRUNCATE_ERRORS % self.errors_table)
        self._db.commit()

    def get_local_mo(self):
        """ write all mo_local def in self state """
        self.qurs1.execute(pg.GET_ALL_LOCAL_MO)
        for _mo in self.qurs1.fetchall():
            self.mo_local[_mo.scode] = _mo.code

    def get_hpm_data(self, get_fresh: bool) -> object:
        self.qurs.execute(
            pg.GET_HPM_DATA,
            (self.talon_tbl, self.cfg.int_month, get_fresh))
        return self.qurs.fetchall()

    def get_npr_mo(self, data: dict) -> int:
        npr = data.get('from_firm', None)
        if npr:
            return self.mo_local.get(npr, None)
        return None

    def get_all_usl(self):
        """ write all usl to self state """
        self.qurs1.execute(pg.GET_ALL_USL, (
            self.talon_tbl, self.para_tbl, self.cfg.int_month))
        for usl in self.qurs1.fetchall():
            if self.usl.get(usl.idcase, None) is None:
                self.usl[usl.idcase] = [usl]
                continue
            # List[ NamedTuple[] ]
            self.usl[usl.idcase].append(usl)

    def get_pmu_usl(self, idcase: int) -> list:
        usl = []
        for _usl in self.usl.get(idcase, []):
            # _usl - Record namedtuple
            usl.append(self.rec_to_dict(_usl))
        return usl

    def get_all_usp(self):
        """ write all spec_usl to self state """
        self.qurs1.execute(pg.GET_SPEC_USL)
        for usl in self.qurs1.fetchall():
            # list of namedtuple
            self.spec_usl[usl.profil] = usl

    def get_spec_usl(self, profil: int) -> list:
        usl = self.spec_usl.get(profil, None)
        if usl is None:
            raise AttributeError(f"Для профиля: {profil} нет специальных услуг")
        return [self.rec_to_dict(usl)]

    def set_error(self, idcase, card, error):
        self.qurs1.execute(pg.SET_ERROR, (idcase, card, error, self.cuser))

    def mark_as_sent(self, idcase):
        #UPDATE talonz_clin_%s SET talon_type=2 WHERE tal_num=%s
        query = pg.MARK_AS_SENT % (str(self.cfg.ye_ar), idcase)
        self.qurs1.execute(query)

    def close(self):
        self.qurs.close()
        self.qurs1.close()
        self._db.commit()
        self._db.close()
