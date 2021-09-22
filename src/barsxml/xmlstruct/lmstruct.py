
from barsxml.xmlmix.maketags import MakeTags
from barsxml.xmlstruct.hdrstruct import HdrData


def lmData(data):

    def _pol(data):
        try:
            return ('w', ['м', 'ж'].index(data.get("pol", '').lower()) + 1)
        except Exception as e:
            return ('w', 0)

    def _dost(data):
        dost = []
        if not bool(data.get("ot", None)):
            dost.append(1)
        if not bool(data.get("fam", None)):
            dost.append(2)
        if not (data.get("im", None)):
            dost.append(3)
        return ('dost', dost)

    def _doc(data):
        if not bool(data["docnum"]) or len(data["docnum"]) == 0:
            for d in ('doctype', 'docnum', 'docser', 'docdate', 'docorg',):
                data[d] = None
        return None

    calc = (
        _pol,
        _dost,
        _doc
    )

    for func in calc:
        t = func(data)
        if t is None:
            continue
        data[ t[0] ] = t[1]

    return data


class LmHdr(HdrData):
    # mo_code: str(6), mo: str(3)
    # year: str(4), month: str(2),
    # pack_type_digit: int(0-9),
    # pack_number: int(0-9),
    # sd_z: int, sumv float
    #
    def __init__(self, mo_code: str, mo: str, year: str, month: str,
                 pack_type_digit: int, pack_number: int, sd_z=None, summ=None):
        super().__init__(mo_code, mo, year, month, pack_type_digit, pack_number)
        self.startTag = '%s\n<PERS_LIST>' % self.xmlVer
        self.endTag = '</PERS_LIST>'
        self.filename = self.l_file
        self.filename1 = self.h_file
        self.version = '3.2'

        self.zglv_tags = (
            'version',
            'data',
            'filename',
            'filename1',
        )
        self.zglv = ('ZGLV', self.zglv_tags)

    def get_schet(self, data):
        return None


class LmPers(MakeTags):

    def __init__(self, mo_code: str, mo: str):
        super().__init__(mo_code, mo)
        self.dubl = []
        self.uniq = set()
        self.pers_tags = (
            'id_pac',
            'fam',
            'im',
            'ot',
            'w',
            'dr',
            'dost',
            'tel',
            'fam_p',
            'im_p',
            'ot_p',
            'w_p',
            'dr_p',
            'dost_p',
            'mr',
            'doctype',
            'docser',
            'docnum',
            'docdate',
            'docorg',
            'snils',
            'okatog',
            'okatop',
            'commentp',
        )
        self.ignore = (
            'mr',
            'snils',
            'okatog',
            'okatop',
            'commentp',
        )
        self.pers = ('pers', self.pers_tags)

    def get_pers(self, data):

        if data["id_pac"] in self.uniq:
            self.dubl.append(data["id_pac"])
            return None

        self.uniq.add(data["id_pac"])
        return self.make_el(self.pers, data)
