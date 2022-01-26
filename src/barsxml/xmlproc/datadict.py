##
from itertools import chain
from collections import UserDict
from barsxml.xmlprod.utils import data_checker, _iddokt
from barsxml.xmlprod.utils import USL_PURP, USL_PRVS, \
    PROFOSM_PURP, SESTRY_PROF, STOM_PROF, SMO_OK, ED_COL_IDSP


class DataDict(UserDict):

    __slots__=('data', 'mo_code', 'pers')

    def __init__(self, mo_code):
        super().__init__()
        self.mo_code = mo_code
        self.pers=set()

    def next_rec(self, data: dict):
        # flush data
        self.data = data

    def pm_data_attrs(self):
        """ here we set additional SLUCH attrs
            'type_pay'
                1 - invoice
                2 - by soul
        """
        if not self.get("type_pay", False):
            self["type_pay"] = 1

        return self


    def hm_data_attrs(self):
        """ calculate ZAP fields
            self: dict
        """
        _visits: int = self["visit_pol"] + self["visit_hom"]

        def _os_sluch():
            return ("os_sluch", None if bool(self["ot"]) else 2)

        def __idsp():# -> int
            # neotl
            if self["for_pom"] == 2:
                return 29

            # stom
            if self["profil"] in STOM_PROF:
                # stom inokray
                if self["smo"] == 0:
                    if _visits == 1:
                        return 29
                    return 30
                # just stom
                return 28

            # profosm or sestry
            if self["purp"] in PROFOSM_PURP or self["profil"] in SESTRY_PROF:
                return 28

            # 4 purp and prvs is USL (all spec issledovanie) inokray incl
            if self["purp"] in USL_PURP and self["prvs"] in USL_PRVS:
                return 28

            # inokray 4 purp
            # if self.purp in HmData.MRT and (self.smo == 0 or self.smo is None):
            #    return 28

            # day stac
            if self["usl_ok"] == 2:
                return 33

            # pocesh
            if _visits == 1:
                return 29

            # obrash
            return 30

        def _idsp():
            return ('idsp', self.get("idsp", __idsp()))

        def _pcel():
            def __pcel(for_pom, purp): # -> str
                if for_pom == 2:
                    return '1.1'  # Посещениe в неотложной форме
                if purp in (1, 2, 6, 9):  # лечебная цель
                    # SMO другой субъект
                    if self["smo_ok"] != SMO_OK:
                        if _visits == 1:
                            return '1.0' # posesh
                        return '3.0' # obrash
                    return '1.2'
                if purp in (3, 10,):  # Диспансерное наблюдение
                    return '1.3'
                if purp in (4, 5, 14, 20, 21):  # Медицинский осмотр
                    return '2.1'
                if purp == 7:  # Патронаж
                    return '2.5'
                return '2.6'  # Посещение по другим обстоятельствам

            return ('p_cel',
                    None if self["usl_ok"] != 3 else __pcel(self["for_pom"], self["purp"]))

        # Диспансерное наблюдение
        def _dn():
            return ('dn', 1 if self["purp"] in (3, 10,)  else None)

        def _vidpom():
            if self.get("vidpom", None):
                return ('vidpom', self["vidpom"])

            if self["profil"] in (78, 82):
                vidpom = 11
                # MTR only since may 2020
                if not self["smo"]:
                    vidpom = 13
            elif self["prvs"] in (76, ) and self["profil"] in (97, 160):
                vidpom = 12
            else:
                vidpom = 13
            return ('vidpom', vidpom)

        def _det():
            return ('det', self.get("det", 0))

        def _summ():
            return ('sum_m', float(self.get("sum_m", 0)))

        def _sumv():
            return ('sumv', float(self.get("sum_m", 0)))

        attrs = (
            _os_sluch,
            _idsp,
            _pcel,
            _dn,
            _vidpom,
            _det,
            _summ,
            _sumv,
        )

        for func in attrs:
            key, value = func()
            self[key] = value

        return self

    def lm_data_attrs(self):

        """ calculate PERS fields
            self: dict
        """

        if self["id_pac"] in self.pers:
            return self

        def _pol():
            try:
                return ('w', ['м', 'ж'].index(self.get("pol", '').lower()) + 1)
            except Exception:
                return ('w', 0)

        def _dost():
            _dost = []
            if not bool(self.get("ot", None)):
                _dost.append(1)
            if not bool(self.get("fam", None)):
                _dost.append(2)
            if not (self.get("im", None)):
                _dost.append(3)
            return ('dost', _dost)

        def _doc():
            if not bool(self["docnum"]) or len(self["docnum"]) == 0:
                for key in ('doctype', 'docnum', 'docser', 'docdate', 'docorg',):
                    self[key] = None

        attrs = (
            _pol,
            _dost,
        )

        for func in attrs:
            key, value = func()
            self[key] = value

        _doc()

        return self

    def data_check(self, nmo: int):
        data_checker(self, int(self.mo_code[3:]), nmo)
        # prepare dict to write
        self.hm_data_attrs().pm_data_attrs().lm_data_attrs()

    def check_usl(self):
        if self["prvs"] in USL_PRVS:
            assert len(self["usl"]) > 0, \
                f'{self["idcase"]}-Для SPEC {self["specfic"]}, PRVS. {self["prvs"]} нет ПМУ'

    def calc_sumv(self):
        sum = 0.0
        ed_col = 0
        for _usl in self["usl"]: #list(dict)
            sum += float(_usl['sumv_usl'])
            ed_col += _usl['kol_usl'] # this is right calculation

        sum += float( self.get("sumv", 0) )
        self["sumv"] = "{0:.2f}".format(sum)

        # now ed_col will be present anyway
        self["ed_col"] = None
        if True: # not data["smo"]:
            if self["idsp"] == 28:
                self["ed_col"] = ed_col
            elif self["idsp"] == 29:
                self["ed_col"]=1

    def set_usl(self, usl: list[dict], usp: list[dict]):
        self["usl"]=[]
        for _usl in chain(usl, usp):
            _usl["lpu"] = self.mo_code

            if _usl.get("profil", None) is None:
                _usl['profil']=self["profil"]

            if _usl.get("det", None) is None:
                _usl["det"] = self.get("det", 0)

            _date1 = _usl.get('date_usl', self['date_1'])
            if _date1 < self["date_1"] or _date1 > self["date_2"]:
                _date1 = self["date_1"]

            _usl['date_in'] = _date1
            if _usl.get('date_out', None) is None:
                _usl['date_out'] = self['date_2']

            _usl['ds'] = self["ds1"]

            if _usl.get('sumv_usl', None) is None:
                _usl['sumv_usl']=0

            _usl['mr_usl_n'] = [{
                'prvs': _usl.get('prvs', self["prvs"]),
                'code_md': _iddokt(
                    self["idcase"],
                    _usl.get('code_md', self["iddokt"])
                )
            }]

            # usp
            if _usl.get('code_usl1', None) is not None:
                if self["idsp"] in (28, 29):
                    _usl['code_usl'] = _usl["code_usl1"]
                else:
                    _usl['code_usl'] = _usl.get("code_usl2", None) or _usl["code_usl1"]
                _usl['kol_usl'] = 1

            # now append this dict
            self["usl"].append(_usl)

        # check for usl
        self.check_usl()

        #then calculate sumv
        self.calc_sumv()

    def set_ksg(self, ksg: dict = {}):
        # will be dropped in tree
        self["ksg_kpg"]=[]

    def get_pers(self):
        if self["id_pac"] in self.pers:
            return None
        self.pers.add(self["id_pac"])
        return self
