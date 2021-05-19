
from datetime import date
from barsxml.xmlmix.maketags import MakeTags


class HdrData(MakeTags):

    def __init__(self, mo: str, year: str, month: str, typ: int, pack: str):
        super().__init__(mo)
        self.xmlVer = '<?xml version="1.0" encoding="windows-1251"?>'
        self.version = '3.1'
        self.lpu = mo
        self.year = f'{year}'
        mnth = int(month)
        self.pack_month = "{0:02d}".format(mnth)
        self.month = f'{mnth}'

        self.file_num = int(pack)
        assert self.file_num < 10, f'File name last digit > 10'
        self.pack_num = f'{typ}{self.file_num}'

        self.code_mo = '250%s' % mo
        self.startTag = '%s\n<ZL_LIST>' % self.xmlVer
        self.endTag = '\n</ZL_LIST>'
        self.data = date.today().isoformat()
        self.file = f'M{self.code_mo}T25_{self.year[2:]}{self.pack_month}{mo}{self.file_num}'
        self.p_file = f'P{self.file}'
        self.h_file = f'H{self.file}'
        self.l_file = f'L{self.file}'
        self.pack_name = f'H{self.code_mo}{self.year[-1]}{self.pack_month}{self.pack_num}.zip'
