""" Postgrest SQL provide implementation, not used case of very slow
    code here is not correct, need to fix
"""

import json
import requests as req
from barsxml.sql.sqlbase import SqlBase
import barsxml.config.pgrestxml as pg


# PostgresT Sql server PROVIDER
class SqlProvider(SqlBase):
    """ BarsXml sql privider """
    def __init__(self, config):
        super().__init__(config)
        self._db = getattr(config.sql, 'SQL_SRV', {}).get('srv', None) # dict
        if self._db is None :
            raise AttributeError("SQL_SRV attribute not provided by Config")
        try:
            req.options(f'{self._db}/doctor', timeout=0.5)
        except req.exceptions.Timeout as exc:
            raise req.exceptions.Timeout(f'DB server {self._db} timeout. {exc}')

        self.usl = {}
        self.spec_usl = {}
        self.mo_local={}
        self.get_local_mo()
        #self.truncate_errors()
        self.talon_tbl = f'{pg.TALONZ_TBL}{self.cfg.ye_ar}'
        self.para_tbl = f'{pg.PARA_TBL}{self.cfg.ye_ar}'

    def truncate_errors(self):
        pass

    def get_local_mo(self):
        """ get_local_mo is a db view """
        _r = req.get(f'{self._db}{pg.GET_ALL_LOCAL_MO}')
        for _mo in _r.json():
            self.mo_local[_mo['scode']] = _mo['code']

    def get_hpm_data(self, get_fresh: bool):
        """ get_hpm_data is a db func """
        data = dict(tbl=self.talon_tbl, mont=self.cfg.int_month, fresh=get_fresh)
        _r = req.post(f'{self._db}{pg.GET_HPM_DATA}', json=data, stream=True)
        def gen():
            decoder = json.JSONDecoder()
            buffer = ''
            for chunk in _r.iter_content(chunk_size=2048, decode_unicode=True):
                buffer += chunk
                try:
                    while buffer:
                        result, index = decoder.raw_decode(buffer)
                        yield result
                        buffer = buffer[index:]
                except ValueError:
                        # Not enough data to decode, read more
                    break
            else:
                _r.close()
        return next(gen())

    def get_npr_mo(self, data: dict) -> int:
        npr = data.get('from_firm', None)
        if npr:
            return self.mo_local.get(npr, None)
        return None

    def get_all_usl(self):
        """ get all usl """
        data = dict(talon_tbl=self.talon_tbl, para_tbl=self.para_tbl, mont=self.cfg.int_month)
        _r = req.post(f'{self._db}{pg.GET_ALL_USL}', json=data)
        for usl in _r.json():
            _id = usl['idcase']
            if self.usl.get(_id, None) is None:
                self.usl[id] = [usl]
                continue
            self.usl[_id].append(usl)

    def get_pmu_usl(self, idcase: int) -> list:
        return self.usl.get(idcase, [])

    def get_all_usp(self) -> list:
        """ usp """
        _r = req.get(f'{self._db}{pg.GET_SPEC_USL}')
        for usl in _r.json():
            self.spec_usl[usl['profil']] = usl

    def get_spec_usl(self, data: dict) -> list:
        return self.spec_usl.get(data['profil'], [])

    def set_error(self, idcase, card, error):
        pass
        #self.qurs1.execute(self.config.SET_ERROR, (idcase, card, error))

    def mark_as_sent(self, data):
        #UPDATE talonz_clin_%s SET talon_type=2 WHERE tal_num=%s
        mark = pg.MARK_WHERE % data['idcase']
        req.patch(f'{self._db}{self.talon_tbl}{mark}', json=pg.MARK_AS_SENT)

    def close(self):
        pass
