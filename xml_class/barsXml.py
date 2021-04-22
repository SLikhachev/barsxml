

import os, zipfile
from tempfile import TemporaryFile as tmpf
from functools import reduce
from barsxml.config.xml_type import TYPES
from barsxml.sql_class.sql_base import get_sql_provider
from barsxml.xml_class.xmlRecords import XmlRecords
from barsxml.xml_class.pmHdrFile import PmHdr, PmSluch
from barsxml.xml_class.hmHdrFile import HmHdr, HmZap
from barsxml.xml_class.lmHdrFile import LmHdr, LmPers
from barsxml.xml_class.mixTags import HdrMix
from barsxml.xml_class.utils import DataObject


class BarsXml(XmlRecords):
    def __init__(self, config: object, type: str, month: str, pack_num: str):
        # type is:
        # app - app 0-1n
        # dsc - day stac 2n
        # onk - onko 3n (C packet)
        # dia - diagnostic 4n
        # sto - stomatolog 5n
        # not used 6n
        # pcr - pcr 7n
        # ifa  ifa 8n
        # tra - travma 9n
        self.pack_type = type  # = (pack_type, pack_digit)
        self.pack_digit = TYPES[type]
        self.mo_code = config.MO_CODE  # string(3) head MO code
        self.xmldir = f"{config.BASE_XML_DIR}\\{type}\\"  # str abs path to save xml file
        self.error_file = f"errors_{type}"
        self.errorFile = None
        self._xpcr = config.PCR
        self._xifa = config.IFA

        self.year = config.YEAR  # string(4) digits
        self.month = month  # string(2) digits
        self.pack = pack_num  # string(2), pack number
        self.ye_ar = self.year[2:]  # last 2 digits

        self.errors = 0
        self.zfile = ''

        # init sql adapter
        self.sql = get_sql_provider(config).SqlProvider(config, self.year, month)

        # init xml objects
        self.pmSluch = PmSluch(self.mo_code)
        self.hmZap = HmZap(self.mo_code)
        self.lmPers = LmPers(self.mo_code)

    def make_xml(self, mark_sent: bool, get_fresh: bool, check=False) -> tuple:
        """
        mark_sent: bool if TRUE set records field talon_type = 2 else ignore
        get_fresh: bool if TRUE ignore already sent and accepted records else get all records
        check: bool if TRUE -> check tables recs only, don't make xml pack
        """
        rc = 0
        rdata = self.sql.get_hpm_data(get_fresh)

        if len(rdata) == 0:
            return self.close(rc)

        self.check = check
        self.errFname = f'{self.xmldir}\\{self.error_file}.txt'
        self.errorFile = open(self.errFname, 'w')  # if test else None

        # make pack anyway if not check, just ignore all errors
        self.pmFile = tmpf(mode="r+") if not self.check else None
        self.hmFile = tmpf(mode="r+") if not self.check else None
        self.lmFile = tmpf(mode="r+", encoding="1251") if not self.check else None

        rc = reduce(self.process(mark_sent), rdata, 0)

        # make ZIP archive
        if rc > 0 and not self.check:
            self.make_zip(rc)

        return self.close(rc)

    def process(self, mark_sent):
        def fp(rc, rdata_row):
            if not self.proper_type(rdata_row):
                return rc

            self.ksg = self.sql.get_ksg_data(rdata_row)  # dict
            nmo = self.get_npr_mo(rdata_row)
            self.usl = self.sql.get_usl(rdata_row)
            # specaial usl for posesh obrasch
            self.usp = self.sql.get_spec_usl(rdata_row)
            try:
                self.data = DataObject(rdata_row, self.mo_code, nmo)
                self.write_sluch()
                self.write_zap()
                self.write_pers()
            except Exception as e:
                self.errorFile.write(f'{rdata_row.idcase}-{e}\n')
                # errors from original rdata_row
                self.sql.set_error(rdata_row.idcase, rdata_row.card, str(e).split('-')[1])
                self.errors += 1
                return rc

            # mark as sent
            if not self.check and mark_sent:
                self.sql.mark_as_sent(rdata_row)
            rc += 1
            return rc

        return fp

    def make_zip(self, rc):
        # make zip file anyway and return it
        to_zip = []
        for f, h in ((self.hmFile, HmHdr), (self.pmFile, PmHdr), (self.lmFile, LmHdr)):
            f.seek(0)
            to_zip.append(self.write_hdr(h, f, sd_z=rc, summ='0.00'))
            f.close()

        hdr = HdrMix(self.mo_code, self.year, self.month, self.pack_digit, self.pack)
        os.chdir(self.xmldir)
        self.zfile = f'{hdr.pack_name}'
        with zipfile.ZipFile(self.zfile, 'w', compression=zipfile.ZIP_DEFLATED) as zipH:
            for f in to_zip:
                zipH.write(f)

    def close(self, rc):
        if bool(self.errorFile):
            self.errorFile.close()

        if self.errors == 0:
            os.remove(self.errFname)
            self.errFname = ''

        # no right records found
        if not bool(rc):
            for f in (self.hmFile, self.pmFile, self.lmFile):
                if f:
                    f.close()

        self.sql.close()

        zipname = "No zip file wrote"
        if len(self.zfile) > 0:
            zipname = os.path.join(self.xmldir, self.zfile)

        # rows wrote, person wrote, zipfile name, errors found
        return rc, len(self.lmPers.uniq), zipname, self.errors
