
from pathlib import Path
import xml.etree.cElementTree as ET
from barsxml.xmlstruct.pmstruct import pmData
from barsxml.xmlstruct.hmstruct import hmData
from barsxml.xmlstruct.lmstruct import lmData
from barsxml.xmlprod.utils import USL_PRVS


class XmlRecords:

    def write_hdr(self, tmpd, hdr, tmp_file, sd_z=0, summ='0.00'):
        # mo_code: str(6), mo: str(3)
        # year: str(4), month: str(2),
        # pack_type_digit: int(0-9),
        # pack_number: int(0-9),
        # sd_z: int, sumv: str('0.00')):
        #
        _hdr = hdr(
            self.mo_code, self.mo, self.year, self.month, self.pack_type_digit, self.pack_number, sd_z, summ)

        _fname = f"{_hdr.filename}.xml"
        _absname = Path(f"{tmpd}") / _fname
        print(_absname)
        with open(_absname, 'w', encoding='1251') as _file:
            _file.write('%s\n' % _hdr.startTag)

            ET.ElementTree(_hdr.get_zag(_hdr)).write(_file, encoding="unicode")
            _file.write('\n')
            schet = _hdr.get_schet(_hdr)  # LM class returns None

            if schet is not None:
                ET.ElementTree(schet).write(_file, encoding="unicode")
                _file.write('\n')

            for line in tmp_file:
                _file.write(line)
            _file.write(_hdr.endTag)
        return _fname

    def write_sluch(self, stom=None):
        # now data is DICT
        data = pmData(self.data)

        if data["prvs"] in USL_PRVS:
            assert len(self.usl) > 0, \
                f'{data["idcase"]}-Случай SL tag : Для SPEC {data["specfic"]}, PRVS. {data["prvs"]} нет ПМУ'

        self.pmSluch.set_usl('usl', self.usl, self.usp)
        if stom and len(stom) > 0:
            self.pmSluch.set_usl('stom', stom)

        sluch = self.pmSluch.get_sluch(data)
        if self.check:
            return
        ET.ElementTree(sluch).write(self.pmFile, encoding="unicode")
        self.pmFile.write('\n')


    def write_zap(self, stom=None):
        # now DICT
        data = hmData(self.data)

        self.hmZap.set_ksg(self.ksg, data)
        self.hmZap.set_usl('usl', self.usl, self.usp, data)

        zap = self.hmZap.get_zap(data)

        if self.check:
            return
        ET.ElementTree(zap).write(self.hmFile, encoding="unicode")
        self.hmFile.write('\n')

    def write_pers(self):
        pers = self.lmPers.get_pers( lmData(self.data) )

        if self.check:
            return
        if pers:
            ET.ElementTree(pers).write(self.lmFile, encoding="unicode")
            self.lmFile.write('\n')

       
