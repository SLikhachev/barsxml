

import os, shutil, zipfile
from time import time
from tempfile import SpooledTemporaryFile as tmpf
#from tempfile import TemporaryFile as tmpf
from tempfile import TemporaryDirectory
# NO reason
#from concurrent.futures import ThreadPoolExecutor, as_completed
#from functools import reduce
from barsxml.config.xmltype import TYPES
from barsxml.path.thispath import Path
from barsxml.sql import get_sql_provider
from barsxml.xmlprod.xmlrecords import XmlRecords
from barsxml.xmlstruct.pmstruct import PmHdr, PmSluch
from barsxml.xmlstruct.hmstruct import HmHdr, HmZap
from barsxml.xmlstruct.lmstruct import LmHdr, LmPers
from barsxml.xmlstruct.hdrstruct import HdrData
from barsxml.xmlprod.utils import data_checker


class BarsXml(XmlRecords):
    def __init__(self, config: object, pack_type: str, mo_code: str, month: str, pack_num: int):
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
        # xml - for simple packages of diagnistic 0
        self.pack_type = pack_type  # string(3)
        self.pack_type_digit = TYPES[pack_type] % 10 # digit 0-9

        # No chek for right code? may be exception
        self.mo_code = mo_code # string MO in 250796 format
        self.mo = mo_code[3:] # last 3 digits i.e 796

        self.xmldir = Path( str(config.BASE_XML_DIR) )
        if len(pack_type) > 0:
            self.xmldir = self.xmldir / pack_type   # str abs path to save xml file

        self.error_file_name = self.xmldir / f"errors_{pack_type}{str(time())[10:14]}.txt"
        self.errorFile = None
        self.errors = 0

        self.year = config.YEAR  # string(4) digits
        self.month = month  # string(2) digits
        self.pack_number = int(pack_num) % 10 # digit 0-9

        self.zfile = ''

        # init sql adapter dependency
        self.sql = get_sql_provider(config).SqlProvider(config, mo_code, self.year, month)

        # init xml objects

    def init_files(self):

        self.pmSluch = PmSluch(self.mo_code, self.mo)
        self.hmZap = HmZap(self.mo_code, self.mo)
        self.lmPers = LmPers(self.mo_code, self.mo)

        self.errorFile = open(self.error_file_name, "w")

        # make pack anyway if not check, just ignore all errors
        self.pmFile = tmpf(mode="r+") if not self.check else None
        self.hmFile = tmpf(mode="r+") if not self.check else None
        self.lmFile = tmpf(mode="r+", encoding="1251") if not self.check else None

    def make_xml(self, mark_sent: bool, get_fresh: bool, check=False) -> tuple:
        """
        mark_sent: bool if TRUE set records field talon_type = 2 else ignore
        get_fresh: bool if TRUE ignore already sent and accepted records else get all records
        check: bool if TRUE -> check tables recs only, don't make xml pack
        """
        self.check = check
        rc = 0
        '''
        if len(rdata) == 0:
            return self.close(rc)
            #raise Exception("Length of the fetched sql data is zero ")
        '''
        self.init_files()
        self.sql.get_all_usp()
        self.sql.get_all_usl()
        rdata = self.sql.get_hpm_data(self.pack_type, get_fresh)

        for rdata_row in rdata:
            data = self.sql.rec_to_dict(rdata_row)
            idcase, card = data['idcase'], data['card']

            self.ksg = self.sql.get_ksg_data(data)  # dict
            nmo = self.sql.get_npr_mo(data) #int

            self.usl = self.sql.get_pmu_usl(idcase)
            # specaial usl for posesh / obrasch
            self.usp = self.sql.get_spec_usl(data)
            try:
                self.data = data_checker(data, int(self.mo), nmo)
                #print(self.data)
                self.write_sluch()
                self.write_zap()
                self.write_pers()
            except Exception as e:
                self.errorFile.write(f'{idcase}-{e}\n')
                # errors from original rdata_row
                self.sql.set_error(idcase, card, str(e).split('-')[1])
                self.errors += 1
                continue

            # mark as sent
            if not self.check and mark_sent:
                self.sql.mark_as_sent(rdata_row)
            rc += 1

        # end loop of all data
        # make ZIP archive
        if rc > 0 and not self.check: #pass
            self.make_zip(rc)

        return self.close(rc)

    def make_zip(self, rc):
        # make zip file anyway and return it
        with TemporaryDirectory() as tmpd:
            to_zip = []
            for fd, hdr in ((self.hmFile, HmHdr), (self.pmFile, PmHdr), (self.lmFile, LmHdr)):
                fd.seek(0)
                to_zip.append(self.write_hdr(tmpd, hdr, fd, sd_z=rc, summ='0.00'))
                fd.close()

            hdr = HdrData(
                self.mo_code, self.mo, self.year, self.month,
                self.pack_type_digit, self.pack_number)
            self.zfile = hdr.pack_name.split('.')[0]
            #self.zfile = f'{hdr.pack_name}'
            #self.pzfile = Path(self.xmldir)  /  self.zfile
            os.chdir(str(self.xmldir))
            #os.chdir(tmpd)
            #with zipfile.ZipFile(self.pzfile, 'w', compression=zipfile.ZIP_DEFLATED) as zipH:
            #    for f in to_zip:
            #       zipH.write(f)

            base_name = Path(self.xmldir)  /  self.zfile
            print(self.xmldir, tmpd, base_name)
            shutil.make_archive(str(base_name), 'zip', tmpd)

    def close(self, rc):
        if bool(self.errorFile):
            self.errorFile.close()
            if self.errors == 0:
                os.remove(self.error_file_name)
                self.error_file_name = ''

        # no right records found
        if not bool(rc):
            for f in ('hmFile', 'pmFile', 'lmFile'):
                fd = getattr(self, f, None)
                if fd:
                    fd.close()

        self.sql.close()

        zipname = self.error_file_name
        if len(str(self.zfile)) > 0:
            zipname = self.xmldir / f'{self.zfile}.zip'

        pers = self.lmPers.uniq if hasattr(self, 'lmPers') else ()
        # rows wrote, person wrote, zipfile name, errors found
        return rc, len(pers), str(zipname), self.errors
