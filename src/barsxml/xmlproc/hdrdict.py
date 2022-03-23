""" module """
from datetime import date
from barsxml.xmlproc.configx import ConfigAttrs


XML='<?xml version="1.0" encoding="windows-1251"?>'


def make_hdr_dict(cfg: ConfigAttrs, sd_z: int =0, summ: str ='0.00'): # -> dict
    """ ConfigAttrs(
            mo_code: str(6),
            mo: str(3)
            year: str(4),
            month: str(2),
            pack_type_digit: int(0-9),
            pack_number: int(0-9)
        )
        sd_z: number of records have been write
        summ: sum of the pack
    """
    month= "{0:02d}".format(int(cfg.month))
    year = cfg.year[2:]
    pack = cfg.pack_number
    file = f'M{cfg.mo_code}T25_{year}{month}{cfg.mo}{pack}'
    code = f'{cfg.mo}{year}{month}'
    data = date.today().isoformat()
    return {
        'code': code,
        'code_mo': cfg.mo_code,
        'lpu': cfg.mo,
        'year': cfg.year,
        'month': int(month),
        'p_file': f'P{file}',
        'h_file': f'H{file}',
        'l_file': f'L{file}',
        'pack_name': f'H{cfg.mo_code}{cfg.year[-1]}{month}{cfg.pack_type_digit}{pack}.zip',
        'xml_tag': XML,
        'data': data,
        'start_tag': f'{XML}\n<ZL_LIST>\n',
        'end_tag': '</ZL_LIST>',
        'sd_z': f'{sd_z}',
        'nschet': f'{code}{pack}',
        'dschet': data,
        'summav': f'{summ}'
    }

def make_hm_hdr( hdr: dict ): #->dict
    """ make """
    hdr["filename"] = hdr["h_file"]


def make_pm_hdr( hdr: dict ): #->dict
    """ make """
    hdr["filename"] = hdr["p_file"]
    hdr["filename1"] = hdr["h_file"]


def make_lm_hdr( hdr: dict ): #->dict
    """ make """
    hdr["start_tag"] = f'{XML}\n<PERS_LIST>\n'
    hdr["end_tag"] = '</PERS_LIST>'
    hdr["filename"] = hdr["l_file"]
    hdr["filename1"] = hdr["h_file"]
