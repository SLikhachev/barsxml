""" module """
from types import SimpleNamespace
import re
from functools import reduce

# XRAY, UZI, ENDOSC, LABGEN, GISTOL
#profil
USL_PROF = (78, 106, 123, 40, 15)

#specfic
USL_SPEC = (63, 10, 85,)

#prvs
USL_PRVS = (31, 48, 60, 81, 93)

# diagnostic purpose
USL_PURP = (4,)

# pofosmotr purpose
PROFOSM_PURP = (21, 22)

#stomatology prifil
STOM_PROF = (85, 86, 87, 88, 89, 90)

#
SESTRY_PROF = (82, 83)

ED_COL_IDSP = (25, 28, 29)

REGION = '250'
SMO_OK = "05000"

class RowObject(SimpleNamespace):
    """ class """
    def __init__(self, row):
        if isinstance(row, dict):
            self.from_dict(row)
        elif hasattr(row, 'cursor_description'):
            self.odbc_row_data(row)
        elif hasattr(row, '_asdict'):
            self.psycopg_row_data(row)
        else:
            raise TypeError(f'Row Object has non supported type: {type(row)}')

    def from_dict(self, data):
        """ from_dict """
        for name, value in data.items():
            setattr(self, name, value)

    def psycopg_row_data(self, data):
        """ row_data """
        for name, value in data._asdict().items():
            setattr(self, name, value)

    def odbc_row_data(self, data):
        """ row data """
        def attrs(idx, desc):
            _d = data[idx]
            if isinstance(_d, float):
                _d = int(_d)
            setattr(self, desc[0], _d)
            idx += 1
            return idx

        reduce(attrs, data.cursor_description, 0)

SNILS = r'^\d{3}-\d{3}-\d{3} \d\d$'
IDDOKT = r'^\d{11}$'

def _iddokt(_id: str, snils: str):
    if re.fullmatch(IDDOKT, snils):
        return snils
    _sl = snils.split('-')
    if len(_sl) == 4:
        _sn = f"{'-'.join(_sl[:3])} {_sl[3]}"
    else:
        _sn = snils
    assert re.fullmatch(SNILS, _sn), \
       f"{_id}-СНИЛС доктора - неверный формат: {_sn}"
    return _sn.replace('-', '').replace(' ', '')
    #return _sn


def _fmt_000(val):
    if val is None:
        return ''
    _v = int(val)
    _s = "{0:03d}".format(_v)
    if len(_s) > 3:
        return _s[-3:]
    return _s


def _date(_id: str, _d: dict):
    '''
        tal.open_date as date_1,
        tal.close_date as date_2,
        tal.crd_num as card,
    '''
    assert _d["date_1"] and _d["date_2"], f'{_id}-Нет даты талона'
    assert _d["date_2"] >= _d["date_1"], f'{_id}-Дата 1 больше даты 2'
    assert _d["card"], f'{_id}-Нет карты талона'


def _smo_polis(_id: str, _d: dict):
    '''
        tal.mek, -- as pr_nov,

        tal.smo as tal_smo,
        tal.polis_type,
        tal.polis_ser,
        tal.polis_num,
        tal.smo_okato,

        crd.smo as smo,
        crd.polis_type as vpolis,
        crd.polis_num as npolis,
        crd.polis_num as id_pac,
        crd.polis_ser as spolis,
        crd.st_okato,
        crd.smo_ogrn,
        crd.smo_okato as smo_ok,
        crd.smo_name as smo_nam,
    '''
    if not _d.get("pr_nov", None):
        _d["pr_nov"] = 1 if bool(_d.get("mek", 0)) else 0

    # set smo, polis from talon
    if _d.get("polis_type", None) is not None and \
        _d.get("polis_num", None) is not None:

        for attr in (
                ("vpolis", "polis_type"),
                ("npolis", "polis_num"),
                ("spolis", "polis_ser"),
                ("smo", "tal_smo"),
                #("smo_ok" , "smo_okato"),
                ("id_pac", "polis_num")):
            _d[ attr[0] ] = _d[ attr[1] ]


    assert _d.get("vpolis", None), f'{_id}-Тип полиса не указан'
    assert _d.get("npolis", None), f'{_id}-Номер полиса не указан'
    if _d["vpolis"] == 1:
        assert _d.get("spolis", None) and _d["npolis"], \
            f'{_id}-Тип полиса не соответвует типу 1 (старый)'
    elif _d["vpolis"] == 2:
        assert len(_d["npolis"]) == 9, \
            f'{_id}-Тип полис не времянка, не соответвует VPOLIS 2 (времянка)'
    elif _d["vpolis"] == 3:
        assert len(_d["npolis"]) == 16, \
            f'{_id}-Тип полис не ЕНП, не соответвует VPOLIS 3 (ЕНП)'
## -------------------------------------
        # as for H VERSION = 3.2 ENP tag
        _d["enp"] = _d["npolis"]
        del _d["npolis"]
## -------------------------------------
    else:
        raise AttributeError(f'{_id}-Тип полиса не поддерживаем')

    # smo is logical False (empty string or zero value)
    smo = _d.get("smo", None)
    if smo is not None and not bool(smo):
        _d["smo"] = None

    # as for H VERSION = 3.2 SMO_OK tag was deleted
    assert _d.get("smo", None) or _d.get("smo_ogrn", None), f'{_id}-Нет ни СМО ни СМО ОГРН'

    try:
        _d["id_pac"] = int(_d["id_pac"])
    except ValueError:
        raise ValueError(f'{_id}-Номер полиса не целое число')


def _purp(_id: str, _d: dict):
    '''
        tal.doc_spec as specfic,

        tal.purp,
        tal.usl_ok,
        tal.for_pom,
        tal.rslt,
        tal.ishod,
    '''
    # assert self.specfic, f'{_id}-SPECFIC ( специальность из регионального справочника) не указан'
    if not _d["purp"]:
        _d["purp"] = 2  # for usl_ok=2
    assert _d[ "usl_ok"], f'{_id}-USL_OK (условия оказания) не указан'
    assert _d[ "for_pom"], f'{_id}-FOR_POM (форма помощи) не указан'
    assert _d[ "rslt"] and _d["ishod"], f'{_id}-RESULT/ISHOD (исход, результат) не указан'


def _visits(_id: str, _d: dict):
    '''
        tal.visit_pol,
        tal.visit_home as visit_hom,
    '''
    if _d["usl_ok"] == 3:
        assert _d["visit_pol"] or _d["visit_hom"], f'{_id}-Нуль количество посещений АПП'  # yet
        return
    if _d["usl_ok"] == 2:
        _d["kd_z"] = _d["visit_ds"] if _d["visit_ds"] else _d["visit_hs"]
        assert _d["kd_z"],  f'{_id}-Нуль количество посещений ДС'
        return
    assert False, f'{_id}- Неверный тип USL_OK для АПП, ДС'

# приняли на консультацию
def _naprav_cons(_id: str, _d: dict):
    '''
        tal.npr_date
        tal.npr_mo as from_firm,
        tal.naprlech,
        tal.nsndhosp,
        tal.d_type,
    '''
    # consultaciya
    if _d["npr_mo"]:
        if _d.get("from_firm", None) is None:
            _d["from_firm"] = _d["npr_mo"][-3:]
        if _d["from_firm"] != _d["mo"]:
            pass
        #    assert d.get("naprlech", False), f'{_id}-Консультация нет Напаравления в другое МО'
        if _d.get("npr_date", None) is None:
            _d["npr_date"] = _d["date_1"]
        return

    # diagnostic planovaya
    if ( int(_d["prvs"]) in USL_PRVS) and int(_d["for_pom"]) == 3:
    # other MO need napravlenie
        # ----------------------
        # this code is a just dirty hack
        # these records need to drop out
        if _d.get("from_firm", None) is None:
            _d["from_firm"] = _d["mo"]
        #  ---------------------
        _d["npr_date"] = _d.get("npr_date", _d["date_1"])
        if _d["from_firm"] != _d["mo"]:
            _d["npr_mo"] = f'{REGION}{_d["from_firm"]}'
            #assert d.get("naprlech", False),
            # f'{_id}-Диагностика, нет Напаравления или МО направления'
        else:
            # diagnostic in self MO no naprav needed
            _d["npr_mo"] = f'{REGION}{_d["mo"]}'

    # DS
    if _d["usl_ok"] == 2:
        assert _d.get("naprlech", False), f'{_id}-ДС, нет Напаравления'
        _d["npr_mo"] = f'{REGION}{_d["mo"]}'
        _d["npr_date"] = _d["date_1"]
        _d["from_firm"] = _d["mo"]

def _naprav_hosp(_id: str, _d: dict):
    # hospital from self MO
    if _d.get("nsndhosp", None) is not None:
        _d["from_firm"] = _d["mo"]


def _diag(_id: str, _d: dict):
    '''
        tal.d_type,
        tal.ds1,
        tal.ds2,
        tal.char1 as c_zab,
    '''

    assert _d["ds1"], f'{_id}-Нет DS1 (основной диагноз)'
    if _d["ds1"].upper().startswith('Z'):
        _d["c_zab"] = None
    else:
        assert _d["c_zab"], f'{_id}-Нет C_ZAB (характер основного заболевания)'


def _doct(_id: str, _d: dict):
    """
        spec.prvs,
        spec.profil,
        doc.snils as iddokt,
    """
    assert _d["prvs"] and _d["profil"], \
        f'{_id}-Нет PRVS | PROFIL (кода специальности по V021, профиля V002)'
    assert _d["iddokt"], f'{_id}-Нет СНИЛС у доктора'
    if _d["prvs"] in USL_PRVS:
        assert _d["purp"] in USL_PURP, \
            f'{_id}-Для спец. {_d["specfic"]}, prvs {_d["prvs"] } неверная цель - {_d["purp"]}'

    # right string may be in database
    #self.iddokt = self.iddokt.replace(" ", "-")
    _d["iddokt"] = _iddokt(_d["idcase"], _d["iddokt"])

    # 2020 FOMS 495 letter
    if (_d["prvs"] in USL_PRVS) and (_d["for_pom"] != 2):
        _d["ishod"] = 4  # 304
        _d["rslt"] = 14  # 314

    if _d["ishod"] < 100:
        _d["ishod"] += _d["usl_ok"] * 100
    if _d["rslt"] < 100:
        _d["rslt"] += _d["usl_ok"] * 100


def _pacient(_id: str, _d: dict):
    '''
    -- PACIENT
        crd.fam,
        crd.im,
        crd.ot,
        crd.gender as pol,
        crd.birth_date as dr,
        crd.dost as dost,
        crd.dul_type as doctype,
        crd.dul_serial as docser,
        crd.dul_number as docnum,
        crd.dul_date as docdate,
        crd.dul_org as docorg
    '''

    assert _d["fam"], f'{_id}-Нет Фамилии пациента'
    assert _d["dr"], f'{_id}-Нет дня рождения пациента'
    if _d["vpolis"] != 3 or _d["smo_ok"] != SMO_OK:
        #print(self.doctype, self.docser, self.docnum)
        assert _d["doctype"] and _d["docnum"] and _d["docser"], \
            f'{_id}-Укажите полностю ДУЛ'
        assert _d.get("docdate", None) and _d.get("docorg", None),\
            f'{_id}-Укажите дату и УФМС ДУЛ'
        if _d["doctype"] and _d["doctype"] == 14: # passport RusFed
            assert re.fullmatch(r'^\d\d \d\d$', _d["docser"]), \
                f'{_id}-Серия паспрота не в формате 99 99: {_d["docser"]}'
            assert re.fullmatch(r'^\d{6}$', _d["docnum"]), \
                f'{_id}-Номер паспорта не 6 цифр'

    # local person no doc_date doc_org needed
    if _d["smo_ok"] == SMO_OK:
        _d["docdate"], _d["docorg"] = None, None
    # self.os_sluch= 2 if self.dost.find('1') > 0 else None

def _d_type(_id: str, _d: dict):
    _d["d_type"] = None
    if _d.get("ot", None) is None:
        _d["d_type"] = 5

def data_checker(data: dict, this_mo: int, napr_mo: int):# -> dict:
    """ data checker """
    data["mo"] = this_mo # int(3) 228
    # in rec we have only from_firm
    data["npr_mo"] = napr_mo  # int(6) 250228 or None
    if data.get("mo_att", None) is None:
        data["mo_att"] = this_mo

    fns = (
        _date,
        _smo_polis,
        _purp,
        _visits,
        _naprav_cons,
        _naprav_hosp,
        _diag,
        _doct,
        _pacient,
        _d_type,
    )
    for func in fns:
        func(data["idcase"], data)
