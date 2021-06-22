
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

class RowObject:
    def __init__(self, row):

        if hasattr(row, 'cursor_description'):
            self.odbc_row_data(row)
        else:
            self.psycopg_row_data(row)

    def psycopg_row_data(self, data):
        if hasattr(data, "_asdict"):
            for name, value in data._asdict().items():
                setattr(self, name, value)

    def odbc_row_data(self, data):
        def attrs(idx, desc):
            d = data[idx]
            if isinstance(d, float):
                d = int(d)
            setattr(self, desc[0], d)
            idx += 1
            return idx

        reduce(attrs, data.cursor_description, 0)


def _iddokt(id, snils):
    sl = snils.split('-')
    if len(sl) == 4:
        sn = f"{'-'.join(sl[:3])} {sl[3]}"
    else:
        sn = snils
    assert re.fullmatch('^\d{3}-\d{3}-\d{3} \d\d$', sn), \
       f"{id}-СНИЛС доктора - неверный формат"
    return sn


def fmt_000(val):
    if val is None:
        return ''
    v = int(val)
    s = "{0:03d}".format(v)
    if len(s) > 3:
        return s[-3:]
    return s


def _date(id, d):
    '''
        tal.open_date as date_1,
        tal.close_date as date_2,
        tal.crd_num as card,
    '''
    assert d["date_1"] and d["date_2"], f'{id}-Нет даты талона'
    assert d["date_2"] >= d["date_1"], f'{id}-Дата 1 больше даты 2'
    assert d["card"], f'{id}-Нет карты талона'


def _smo_polis(id, d):
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
    if not d.get("pr_nov", None):
        d["pr_nov"] = 1 if bool(d.get("mek", 0)) else 0

    # set smo, polis from talon
    if d.get("polis_type", None) is not None and \
        d.get("polis_num", None) is not None:

        for attr in (
                ("vpolis", "polis_type"),
                ("npolis", "polis_num"),
                ("spolis", "polis_ser"),
                ("smo", "tal_smo"),
                ("smo_ok" , "smo_okato"),
                ("id_pac", "polis_num")):
            d[ attr[0] ] = d[ attr[1] ]


    assert d.get("vpolis", None), f'{id}-Тип полиса не указан'
    assert d.get("npolis", None), f'{id}-Номер полиса не указан'
    if d["vpolis"] == 1:
        assert d.get("spolis", None) and d["npolis"], \
            f'{id}-Тип полиса не соответвует типу 1 (старый)'
    elif d["vpolis"] == 2:
        assert len(d["npolis"]) == 9, \
            f'{id}-Тип полис не времянка, не соответвует VPOLIS 2 (времянка)'
    elif d["vpolis"] == 3:
        assert len(d["npolis"]) == 16, \
            f'{id}-Тип полис не ЕНП, не соответвует VPOLIS 3 (ЕНП)'
    else:
        raise AttributeError(f'{id}-Тип полиса не поддерживаем')

    assert d.get("smo", None) or d.get("smo_ok", None), f'{id}-Нет ни СМО ни СМО ОКАТО'

    smo = d.get("smo", None)
    if smo is not None and not bool(smo):
        d["smo"] = None

    try:
        d["id_pac"] = int(d["id_pac"])
    except ValueError:
        raise ValueError(f'{id}-Номер полиса не целое число')


def _purp(id, d):
    '''
        tal.doc_spec as specfic,

        tal.purp,
        tal.usl_ok,
        tal.for_pom,
        tal.rslt,
        tal.ishod,
    '''
    # assert self.specfic, f'{id}-SPECFIC ( специальность из регионального справочника) не указан'
    if not d["purp"]:
        d["purp"] = 2  # for usl_ok=2
    assert d[ "usl_ok"], f'{id}-USL_OK (условия оказания) не указан'
    assert d[ "for_pom"], f'{id}-FOR_POM (форма помощи) не указан'
    assert d[ "rslt"] and d["ishod"], f'{id}-RESULT/ISHOD (исход, результат) не указан'


def _visits(id, d):
    '''
        tal.visit_pol,
        tal.visit_home as visit_hom,
    '''
    if d["usl_ok"] == 3:
        assert d["visit_pol"] or d["visit_hom"], f'{id}-Нуль количество посещений АПП'  # yet
        return
    if d["usl_ok"] == 2:
        d["kd_z"] = d["visit_ds"] if d["visit_ds"] else d["visit_hs"]
        assert d["kd_z"],  f'{id}-Нуль количество посещений ДС'
        return
    assert False, f'{id}- Неверный тип USL_OK для АПП, ДС'

# приняли на консультацию
def _naprav_cons(id, d):
    '''
        tal.npr_date 
        tal.npr_mo as from_firm,
        tal.naprlech,
        tal.nsndhosp,
        tal.d_type,
    '''
    # consultaciya
    if d["npr_mo"]:
        if d.get("from_firm", None) is None:
            d["from_firm"] = d["npr_mo"][-3:]
        if d["from_firm"] != d["mo"]:
            pass
        #    assert d.get("naprlech", False), f'{id}-Консультация нет Напаравления в другое МО'
        if d.get("npr_date", None) is None:
            d["npr_date"] = d["date_1"]
        return
    
    # diagnostic planovaya
    if ( int(d["prvs"]) in USL_PRVS) and int(d["for_pom"]) == 3:
    # other MO need napravlenie
        # ----------------------
        # this code is a just dirty hack
        # these records need to drop out 
        if d.get("from_firm", None) is None:
            d["from_firm"] = d["mo"]
        #  ---------------------
        d["npr_date"] = d.get("npr_date", d["date_1"])
        if d["from_firm"] != d["mo"]:
            d["npr_mo"] = f'{REGION}{d["from_firm"]}'
            #assert d.get("naprlech", False), f'{id}-Диагностика, нет Напаравления или МО направления'
        else:
            # diagnostic in self MO no naprav needed
            d["npr_mo"] = f'{REGION}{d["mo"]}'

    # DS
    if d["usl_ok"] == 2:
        assert d.get("naprlech", False), f'{id}-ДС, нет Напаравления'
        d["npr_mo"] = f'{REGION}{d["mo"]}'
        d["npr_date"] = d["date_1"]
        d["from_firm"] = d["mo"]
    
def _naprav_hosp(id, d):
    # hospital from self MO
    if d.get("nsndhosp", None) is not None:
        d["from_firm"] = d["mo"]


def _diag(id, d):
    '''
        tal.d_type,
        tal.ds1,
        tal.ds2,
        tal.char1 as c_zab,
    '''

    assert d["ds1"], f'{id}-Нет DS1 (основной диагноз)'
    if d["ds1"].upper().startswith('Z'):
        d["c_zab"] = None
    else:
        assert d["c_zab"], f'{id}-Нет C_ZAB (характер основного заболевания)'


def _doct(id, d):
    """
        spec.prvs,
        spec.profil,
        doc.snils as iddokt,
    """
    assert d["prvs"] and d["profil"], f'{id}-Нет PRVS | PROFIL (кода специальности по V021, профиля V002)'
    assert d["iddokt"], f'{id}-Нет СНИЛС у доктора'
    if d["prvs"] in USL_PRVS:
        assert d["purp"] in USL_PURP, \
            f'{id}-Для спец. {d["specfic"]}, prvs { d["prvs"] } неверная цель - {d["purp"]}'

    # right string may be in database
    #self.iddokt = self.iddokt.replace(" ", "-")
    d["iddokt"] = _iddokt(d["idcase"], d["iddokt"])

    # 2020 FOMS 495 letter
    if (d["prvs"] in USL_PRVS) and (d["for_pom"] != 2):
        d["ishod"] = 4  # 304
        d["rslt"] = 14  # 314

    if d["ishod"] < 100:
        d["ishod"] += d["usl_ok"] * 100
    if d["rslt"] < 100:
        d["rslt"] += d["usl_ok"] * 100


def _pacient(id, d):
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

    assert d["fam"], f'{id}-Нет Фамилии пациента'
    assert d["dr"], f'{id}-Нет дня рождения пациента'
    if d["vpolis"] != 3:
        #print(self.doctype, self.docser, self.docnum)
        assert d["doctype"] and d["docnum"] and d["docser"], \
            f'{id}-Тип полиса не ЕНП и неуказан полностью ДУЛ'
        if d["smo_ok"] != SMO_OK:
            assert d.get("docdate", None) and d.get("docorg", None), f'{id}-Инокраевой без даты и УФМС паспорта'
        if d["doctype"] and d["doctype"] == 14: # pass RF
            assert re.fullmatch('^\d\d \d\d$', d["docser"]), \
                f'{id}-Серия паспрота не в формате 99 99: {d["docser"]}'
            assert re.fullmatch('^\d{6}$', d["docnum"]), \
                f'{id}-Номер паспорта не 6 цифр'

    # local person no doc_date doc_org needed
    if bool(d["smo"]):
         d["docdate"], d["docorg"] = None, None
    # self.os_sluch= 2 if self.dost.find('1') > 0 else None

def _d_type(id, d):
    d["d_type"] = None 
    if d.get("ot", None) is None:
        d["d_type"] = 5 
    

def rec_to_dict(rec):
    if hasattr(rec, "_asdict"):
        return rec._asdict()
    if hasattr(rec, "cursor_description"):
        drec= {}
        for idx, desc in enumerate(rec.cursor_description):
            d = rec[idx]
            if isinstance(d, float):
                d = int(d)
            drec[ desc[0] ] = d
        return drec
    raise AttributeError( "Can't transform Record to Dict" )


def data_checker(rec, mo_code, napr_mo):
    d= rec_to_dict(rec)

    d["mo"] = mo_code # str(3) 228
    # in rec we have only from_firm
    d["npr_mo"] = napr_mo  # str(6) 250228 or None
    if d.get("mo_att", None) is None:
        d["mo_att"] = mo_code 
    """
    if d.get("from_firm", None) is None:
        d["from_firm"] = mo_code
    """
    
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
        _d_type
    )
    for func in fns:
        func(d["idcase"], d)
    return d

