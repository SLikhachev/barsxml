""" The module contains a base checks/validators/calculators
    for main record to produce xmls
"""

# from collections import namedtuple
from types import SimpleNamespace
import re
from functools import reduce
from datetime import date


# XRAY, UZI (ultra sonic reserach), ENDOSCOPY, LABGENETICS, GISTOLoGY
# PROFIL med profils as of V002
USL_PROF = (78, 106, 123, 40, 15)

# SPECFIC med speciality to interrest
USL_SPEC = (63, 10, 85,)

# PRVS doctor's spec flags
USL_PRVS = (31, 48, 60, 81, 93)

# PURP diagnostic purpose
USL_PURP = (4,)

# PURP profosmotr purpose
PROFOSM_PURP = (21, 22)

# PROFIL stomatology prifil
STOM_PROF = (85, 86, 87, 88, 89, 90)

# PROFIL nurses
SESTRY_PROF = (82, 83)

# IDSP Pay profil
ED_COL_IDSP = (25, 28, 29)

REGION = '250'
SMO_OK = "05000"

# pacient CBO status 0 -none 35-svo solder 65- svo solder's family member
PAC_SOC = (0, 35, 65)

# Pacient VZ status
#vz_age=NamedTuple('vz', 'age')
STUDENT=24
WORKER=65
PAC_VZ = {
    "worker": 1,
    "solder": 2,
    "retired": 3,
    "student": 4,
    "unemployed": 5,
    "other":6
}

SNILS = r'^\d{3}-\d{3}-\d{3} \d\d$'
IDDOKT = r'^\d{11}$'

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
        """
        Populate the attributes of the object with key-value pairs from a dictionary.

        :param data: A dictionary containing attribute names as keys and their corresponding values.
        """
        for name, value in data.items():
            # Set each item in the dictionary as an attribute of the object
            setattr(self, name, value)

    def psycopg_row_data(self, data):
        """
        Populate the attributes of the object with key-value pairs
        from a named tuple returned by psycopg2.

        :param data: A named tuple containing attribute names as keys
                     and their corresponding values.
        """
        for name, value in data._asdict().items():
            # Set each item in the named tuple as an attribute of the object
            setattr(self, name, value)

    def odbc_row_data(self, data):
        """
        Populate the attributes of the object with key-value pairs from
        an ODBC row data object.

        :param data: An ODBC row data object containing attribute names as keys
                     and their corresponding values.
        """
        def attrs(idx, desc):
            """
            Set an attribute of the object from an ODBC row data object.

            :param idx: Index of the ODBC row data object to set.
            :param desc: Tuple containing the attribute name and description.
            """
            _d = data[idx]
            if isinstance(_d, float):
                _d = int(_d)
            setattr(self, desc[0], _d)
            idx += 1
            return idx

        # Iterate over the ODBC row data object and set each attribute
        reduce(attrs, data.cursor_description, 0)

def _iddokt(_id: str, snils: str):
    """
    Format given SNIILS in correct form for further processing.

    :param _id: Unique identifier of the record being processed.
    :param snils: SNIILS of the doctor which needs to be formatted.
    :return: Formatted SNIILS as a string.
    """
    if re.fullmatch(IDDOKT, snils):
        return snils

    _sl = snils.split('-')
    if len(_sl) == 4:
        # If SNIILS is given in format 'XXX-XXX-XXXX XXXX',
        # split it into two parts and join them with a space in between.
        _sn = f"{'-'.join(_sl[:3])} {_sl[3]}"
    else:
        # If SNIILS is given in format 'XXXXXXXXXXX', just assign it.
        _sn = snils

    # Check that the SNIILS is in a correct format.
    assert re.fullmatch(SNILS, _sn), \
       f"{_id}-СНИЛС доктора - неверный формат: {_sn}"

    # Remove all spaces and dashes from the SNIILS.
    return _sn.replace('-', '').replace(' ', '')


def _fmt_000(val):
    ''' Format given value as 3 digits zero padded string
        If given value is None, return empty string
        If given value is a string, interpret it as a number
        If given value is a number, format it as 3 digits zero padded string
        If formatted string is longer that 3 characters, return last 3 characters
    '''
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
    #if _d.get("pr_nov", None):
    _d["pr_nov"] = 1 if _d.get("mek", None) else 0

    # set smo, polis from talon
    if _d.get("polis_type", None) and _d.get("polis_num", None):

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

    # if smo is logical False (None, empty string or zero value)
    if not _d.get("smo", None):
        _d["smo"] = None

    # as for H VERSION = 3.2 SMO_OK tag was deleted
    assert _d.get("smo", None) or _d.get("smo_ogrn", None), f'{_id}-Нет ни СМО ни СМО ОГРН'

    try:
        _d["id_pac"] = int(_d["id_pac"])
    except ValueError as exc:
        raise ValueError(f'{_id}-Номер полиса не целое число') from exc


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
    if _d["usl_ok"] == 3: # АПП
        assert _d["visit_pol"] or _d["visit_hom"], f'{_id}-Нуль количество посещений АПП'  # yet
        return

    if _d["usl_ok"] == 2: # ДС
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

    if _d.get("naprlech", None):
        assert len(str(_d["naprlech"])) < 16, f"{_id}-Номер направления слишком длинный"

    # consultaciya
    if _d.get("npr_mo", None):

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

"""
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
    crd.dul_org as docorg,
    crd.mo_att,
    crd.soc,
    crd.vz
"""

def _pac_name(_id: str, _d: dict):
    assert _d["fam"], f'{_id}-Нет Фамилии пациента'
    assert _d["dr"], f'{_id}-Нет даты рождения пациента'
    # check geneder
    if _d.get("gender", False):
        #print("dadat: ", _d["gender"])
        pol = (_d["gender"] == "male" and _d["pol"] == 'м') or (_d["gender"] == "female" and _d["pol"] == 'ж')
        assert pol, f'{_id}-Проверте пол пациента'

    soc = int( _d.get("soc", 0) or 0 )
    assert soc in PAC_SOC, f'{_id}-Неверный код SOC статуса пациента'
    _d["soc"] = _fmt_000(soc)

def _pac_doc(_id: str, _d: dict):
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

    # for local person doc_date doc_org do not needed
    # AND set MO_PR if any
    _d["mo_pr"] = None # Inokraevoy
    if _d["smo_ok"] == SMO_OK:
        _d["docdate"], _d["docorg"] = None, None

        # assert mo_att is set for local pacient
        assert _d.get("mo_att", None), f'{_id}-Укажите код МО прикрепления пациента'
        _d["mo_pr"] = f'{REGION}{_d["mo_att"]}'

    # self.os_sluch= 2 if self.dost.find('1') > 0 else None

def _pac_vz(_id: str, _d: dict):
    """ Calculate Vid zanyatosti """
    if _d.get("vz", None) and _d["vz"] in PAC_VZ.values():
        return
    # date_birth = datetime.strptime(_d["dr"], '%Y-%m-%d').date()
    assert isinstance(_d["dr"], date), f'{_id}-Дата рождения должна быть экземпляром класса date'
    today= date.today()
    age = today.year - _d["dr"].year - ((today.month, today.day) < (_d["dr"].month, _d["dr"].day))
    _d["vz"]= PAC_VZ["retired"]
    if STUDENT > age:
        _d["vz"] = PAC_VZ["student"]
    elif WORKER > age:
        _d["vz"] = PAC_VZ["worker"]
    # print(f'{age}-Возраст {_d["vz"]}- VZ')

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
        _pac_name,
        _pac_doc,
        _pac_vz,
        _d_type,
    )
    for func in fns:
        func(data["idcase"], data)
