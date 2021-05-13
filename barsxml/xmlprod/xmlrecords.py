

import xml.etree.cElementTree as ET
from barsxml.xmlstruct.pmstruct import pmData
from barsxml.xmlstruct.hmstruct import hmData
from barsxml.xmlstruct.lmstruct import lmData
from barsxml.xmlprod.utils import USL_PRVS


class XmlRecords:

    def write_hdr(self, hdr, tmp_file, sd_z=0, summ='0.00'):
        _hdr = hdr(self.mo_code, self.year, self.month, self.pack_digit, self.pack, sd_z, summ)
        _fname = f"{_hdr.filename}.xml"
        _absname = f"{self.xmldir}\\{_fname}"

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
        # now DICT
        data = pmData(self.data)
        '''
        assert (data.specfic in dcons) and len(
            usl) > 0, f'{data.idcase}-Для спец. {data.specfic} нет ПМУ'
        '''
        if data["prvs"] in USL_PRVS:
            assert len(self.usl) > 0, \
                f'{data["idcase"]}-Случай SL tag : Для SPEC {data["specfic"]}, PRVS. {data["prvs"]} нет ПМУ'

        self.pmSluch.set_usl('usl', data, self.usl, self.usp)
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

        # if data.q_u == 3:
        #    hm.reset_ksg()

    def write_pers(self):
        pers = self.lmPers.get_pers( lmData(self.data) )

        if self.check:
            return
        if pers:
            ET.ElementTree(pers).write(self.lmFile, encoding="unicode")
            self.lmFile.write('\n')

       
