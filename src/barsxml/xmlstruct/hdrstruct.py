
from datetime import date
from barsxml.xmlmix.maketags import MakeTags


class HdrData(MakeTags):
    # mo_code: str(6), mo: str(3)
    # year: str(4), month: str(2),
    # pack_type_digit: int(0-9),
    # pack_number: int(0-9)
    #
    def __init__(self, mo_code: str, mo: str, year: str, month: str, pack_type_digit: int, pack_number: int):
        super().__init__(mo_code, mo)
        self.xmlTag = '<?xml version="1.0" encoding="windows-1251"?>'
        self.version = '3.2'
        self.lpu = mo
        self.year = year
        imonth = int(month)
        self.pack_month = "{0:02d}".format(imonth)
        self.month = f'{imonth}'
        self.pack_num = f'{pack_type_digit}{pack_number}'

        self.code_mo = mo_code
        self.startTag = f'{self.xmlTag}\n<ZL_LIST>'
        self.endTag = '\n</ZL_LIST>'
        self.data = date.today().isoformat()
        self.file = f'M{self.code_mo}T25_{self.year[2:]}{self.pack_month}{mo}{pack_number}'
        self.p_file = f'P{self.file}'
        self.h_file = f'H{self.file}'
        self.l_file = f'L{self.file}'
        self.pack_name = f'H{self.code_mo}{self.year[-1]}{self.pack_month}{self.pack_num}.zip'
