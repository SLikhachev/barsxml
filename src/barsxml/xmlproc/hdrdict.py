""" xml files' headers makers """

from datetime import date
from barsxml.xmlproc.configx import ConfigAttrs

# so, start string
XML='<?xml version="1.0" encoding="windows-1251"?>'


def make_hdr_dict(cfg: ConfigAttrs, sd_z: int =0, summ: str ='0.00') -> dict:
    """ @param: cfg attrs:
            mo_code: str(6),
            short_mo: str(3) last 3 digits,
            year: int (full year)
            ye_ar: int (last 2 digits)
            month: str (2),
            int_month: int of month,
            pack_type_digit: int(0-9),
            pack_number: int(0-9)
        @param: sd_z: number of records have been write
        @param: summ: sum of the pack

        return dict: for XmlWriter.write_hdr_body method
    """
    month= "{0:02d}".format(cfg.int_month) # str(2)
    _year = str(cfg.ye_ar) # str(2)
    pack = cfg.pack_number # int(1)

    # TODO `T25_` must_ be rewritten
    file = f'M{cfg.mo_code}T25_{_year}{month}{cfg.short_mo}{pack}'
    code = f'{cfg.short_mo}{_year}{month}'
    data = date.today().isoformat()
    return {
        'code': code,
        'code_mo': cfg.mo_code,
        'lpu': cfg.short_mo,
        'year': str(cfg.year),
        'month': cfg.int_month,
        'p_file': f'P{file}',
        'h_file': f'H{file}',
        'l_file': f'L{file}',
        'pack_name': f'H{cfg.mo_code}{_year[1]}{month}{cfg.pack_type_digit}{pack}.zip',
        'xml_tag': XML,
        'data': data,
        'start_tag': f'{XML}\n<ZL_LIST>\n',
        'end_tag': '</ZL_LIST>',
        'sd_z': f'{sd_z}',
        'nschet': f'{code}{pack}',
        'dschet': data,
        'summav': f'{summ}'
    }

def make_hm_hdr( hdr: dict ):
    """ HM file """
    hdr["filename"] = hdr["h_file"]


def make_pm_hdr( hdr: dict ):
    """ PM file """
    hdr["filename"] = hdr["p_file"]
    hdr["filename1"] = hdr["h_file"]


def make_lm_hdr( hdr: dict ):
    """ LM file """
    hdr["start_tag"] = f'{XML}\n<PERS_LIST>\n'
    hdr["end_tag"] = '</PERS_LIST>'
    hdr["filename"] = hdr["l_file"]
    hdr["filename1"] = hdr["h_file"]
