
import json
import requests as req
from barsxml.sql.sqlbase import SqlBase
import barsxml.config.pgrestxml as pg


# PostgresT Sql server PROVIDER
class SqlProvider(SqlBase):
    
    def __init__(self, config, mo_code, year, month):
        super().__init__(config, mo_code, year, month)
        self.db = getattr(config, 'SQL_SRV', {}).get('srv', None) # dict
        if self.db is None :
             raise AttributeError("SQL_SRV attribute not provided by Config")
        try:
            req.options(f'{self.db}/doctor', timeout=0.5)
        except req.exceptions.Timeout as e:
            raise req.exceptions.Timeout(f'DB server {self.db} timeout. {e}')

        self.usl = {}
        self.spec_usl = {}
        self.mo_local={}
        self.get_local_mo()
        #self.truncate_errors()
        self.talon_tbl = f'{pg.TALONZ_TBL}{self.ye_ar}'
        self.para_tbl = f'{pg.PARA_TBL}{self.ye_ar}'

    def truncate_errors(self):
        pass

    def get_local_mo(self):
        r = req.get(f'{self.db}{pg.GET_ALL_LOCAL_MO}')
        for mo in r.json():
            self.mo_local[mo['scode']] = mo['code']

    def get_hpm_data(self, type: str, get_fresh: bool) -> object:
        data = dict(tbl=self.talon_tbl, mont=int(self.month), fresh=get_fresh)
        r = req.post(f'{self.db}{pg.GET_HPM_DATA}', json=data, stream=True)
        def gen():
            decoder = json.JSONDecoder()
            buffer = ''
            for chunk in r.iter_content(chunk_size=2048, decode_unicode=True):
                buffer += chunk
                while buffer:
                    try:
                        result, index = decoder.raw_decode(buffer)
                        yield result
                        buffer = buffer[index:]
                    except ValueError:
                        # Not enough data to decode, read more
                        break
            else:
                r.close()
        return next(gen())

    def get_npr_mo(self, data: dict) -> int or None:
        npr = data.get('from_firm', None)
        if npr:
            return self.mo_local.get(npr, None)
        return None

    def get_all_usl(self):
        data = dict(talon_tbl=self.talon_tbl, para_tbl=self.para_tbl, mont=int(self.month))
        r = req.post(f'{self.db}{pg.GET_ALL_USL}', json=data)
        for usl in r.json():
            id = usl['idcase']
            if self.usl.get(id, None) is None:
                self.usl[id] = [usl]
                continue
            self.usl[id].append(usl)

    def get_pmu_usl(self, idcase: int) -> list:
        return self.usl.get(idcase, [])

    def get_all_usp(self):
        r = req.get(f'{self.db}{pg.GET_SPEC_USL}')
        for usl in r.json():
            self.spec_usl[usl['profil']] = usl
    
    def get_spec_usl(self, data: dict) -> list:
        return self.spec_usl.get(data['profil'], [])
        
    def set_error(self, idcase, card, error):
        pass
        #self.qurs1.execute(self.config.SET_ERROR, (idcase, card, error))
            
    def mark_as_sent(self, data):
        #UPDATE talonz_clin_%s SET talon_type=2 WHERE tal_num=%s
        mark = pg.MARK_WHERE % data['idcase']
        req.patch(f'{self.db}{self.talon_tbl}{mark}', json=pg.MARK_AS_SENT)

    def close(self):
        pass
