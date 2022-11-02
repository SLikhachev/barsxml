""" This class is used as source of some common attrubutes
    which are used during xml building
"""
import re
from barsxml.path.thispath import Path
from barsxml.config.xmltype import TYPES


class ConfigAttrs:
    """ state object of the common configs """
    def __init__(self, config: object,
        pack_type: str, mo_code: str, month: str, pack_num: int):
        """
            @param: config - config object where
                SQL_PROVIDER, # String
                sql_srv, # dict
                year, #String
                base_xml_dir

            @param: pack_type string of key for TYPES dict('type': int)
                where int is first digit in two last one of 'Tn' in the pack name
                    (n is a sequential pack number in pack series) and T is
                    app - ambulance: 0 | 1
                    dsc - daily stacionar: 2
                    onk - onkology: 3 (C packet)
                    dia - diagnostic: 4
                    sto - stomatolog: 5
                        not used: 6
                    pcr - pcr (covid-19 pcr test): 7
                    ifa - ifa (covid-19 ifa test): 8
                    tra - travmatology: 9
                    xml - for simple packages of diagnistic: 0
            @param: mo_code - code of MO '250799'
            @param: month - pack month '01'-'12'
            @param: pack_num - sequential pack number
        """

        # write all sql (provider and connection dict) to sql attr
        self.sql_srv = config.sql_srv
        self.xmldir = Path( str(config.base_xml_dir) )

        assert pack_type in TYPES.keys(), f"Тип пакета {pack_type} не поддерживается"
        self.pack_type = pack_type  # string(3)
        if len(pack_type) > 0:
            self.xmldir = self.xmldir / pack_type   # str abs path to save xml file
        self.pack_type_digit = TYPES[pack_type]

        try:
            self.mo_code = re.search(r'^\d{6,}$', mo_code).group(0)
            self.short_mo = mo_code[3:] # last 3 digits i.e 796
        except AttributeError:
            raise AttributeError(f"Код МО: {mo_code} не соответвует шаблону") from None

        try:
            self.year = re.search(r'^\d{2,4}$', config.year).group(0)
            self.ye_ar= self.year
            if len(self.year) > 2:
                self.ye_ar= self.year[-2:]
            self.ye_ar= int(self.ye_ar)
            self.year= 2000 + self.ye_ar
        except AttributeError:
            raise AttributeError(f"Год отчета: {config.year} указан неверно") from None
        # max.min excludes 0
        try:
            self.int_month= min(
                int(re.search(r'^\d{1,2}$', month).group(0)),
                12
            )
            self.int_month = max(1, self.int_month) # int
            self.month = month # string
        except AttributeError:
            raise AttributeError(f"Месяц отчета: {month} указан неверно") from None

        try:
            # max.min excludes 0
            self.pack_number = max(1, min(abs(int(pack_num)), 9))
        except ValueError:
            raise ValueError(f"Некорректный номер пакета: {pack_num}") from None
