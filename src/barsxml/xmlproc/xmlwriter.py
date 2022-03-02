""" XmlWRiter class definition"""

import os
import shutil
from time import time
from pathlib import Path
from tempfile import SpooledTemporaryFile as tmpf
#from tempfile import TemporaryFile as tmpf
from tempfile import TemporaryDirectory
import xml.etree.cElementTree as ET
from barsxml.xmlmix.maketags import XmlTreeMaker
from barsxml.xmlstruct.hmxml import HmStruct as hmNS
from barsxml.xmlstruct.pmxml import PmStruct as pmNS
from barsxml.xmlstruct.lmxml import LmStruct as lmNS
from barsxml.xmlproc.configx import ConfigAttrs
from barsxml.xmlproc.hdrdict import make_hdr_dict
from barsxml.xmlproc.hdrdict import make_hm_hdr, make_pm_hdr, make_lm_hdr


class XmlWriter:
    """ calss XmlWriter """
    Ns = ('hm', 'pm', 'lm')
    NsTags = (hmNS.ZAP, pmNS.SLUCH, lmNS.PERS)
    HdrNsFn = (
        (make_hm_hdr, hmNS),
        (make_pm_hdr, pmNS),
        (make_lm_hdr, lmNS)
    )

    def __init__(self, cfg: ConfigAttrs):
        self.cfg = cfg
        self.xmldir = cfg.xmldir
        self.zfile_name = ''
        self.hdr = {}
        self.check = True
        self.ns_files = []

        self.xml = XmlTreeMaker(cfg.mo_code, cfg.mo)

        error_file_name = cfg.xmldir / \
            f"errors_{cfg.pack_type}{str(time())[10:14]}.txt"
        self.error_fd = open(error_file_name, "w", encoding='utf-8')

    def init_files(self, check: bool):
        """ opens tmp files for write report """
        self.check = check
        if check:
            return
        self.ns_files = [tmpf(mode="r+", encoding="1251") for _ in self.Ns]

    def write_error(self, error: str):
        """ write error """
        self.error_fd.write(error)

    def write_hdr_body(self, tmpdir: TemporaryDirectory, hdr_ns: str):
        """ write hdr body to file """
        ns_idx = self.Ns.index(hdr_ns)
        make_hdr_fn, cns = self.HdrNsFn[ns_idx]

        make_hdr_fn(self.hdr)

        _fname = f'{self.hdr["filename"]}.xml'
        _absname = Path(f"{tmpdir}") / _fname
        # print(_absname)

        with open(_absname, 'w', encoding='1251') as hdr_file:
            hdr_file.write(f'{self.hdr["start_tag"]}')

            ET.ElementTree(
                self.xml.make_tree(hdr_ns, cns.ZGLV, self.hdr)
            ).write(hdr_file, encoding="unicode")
            hdr_file.write('\n')

            if hasattr(cns, 'SCHET'):
                ET.ElementTree(
                    self.xml.make_tree(hdr_ns, cns.SCHET, self.hdr)
                ).write(hdr_file, encoding="unicode")
                hdr_file.write('\n')

            # flush tmp file body
            body_file = self.ns_files[ns_idx]
            body_file.seek(0)
            for line in body_file:
                hdr_file.write(line)
            body_file.close()
            hdr_file.write(self.hdr["end_tag"])

        return _fname

    def write_data(self, data):
        """ write data to file """
        #add person to set
        pers = data.get_pers()
        if self.check:
            return  # no IO required
        for idx, cns in enumerate(self.Ns):
            if cns == 'lm' and pers is None:
                continue
            file = self.ns_files[idx]
            ET.ElementTree(
                self.xml.make_tree(cns, self.NsTags[idx], data)
            ).write(file, encoding="unicode")
            file.write('\n')

    def make_zip(self, rcnt):
        """ make zip file anyway and return it """
        with TemporaryDirectory() as tmpdir:
            self.hdr = make_hdr_dict(self.cfg, sd_z=rcnt, summ='0.00')
            to_zip = [self.write_hdr_body(tmpdir, cns) for cns in self.Ns]
            # print(to_zip)
            assert len(to_zip) == 3, f"Ошибка формирования файлов {to_zip}"

            self.zfile_name = self.hdr["pack_name"].split('.')[0]

            os.chdir(str(self.xmldir))
            base_name = Path(self.xmldir) / self.zfile_name
            #print(self.xmldir, tmpdir, base_name)

            shutil.make_archive(str(base_name), 'zip', tmpdir)

    def close(self, rcnt: int, pers: int, errors: int):
        """ close open files """
        if not self.error_fd.closed:
            self.error_fd.close()
            if errors == 0:
                os.remove(self.error_fd.name)

        # close file anyway
        for file in self.ns_files:
            if not file.closed:
                file.close()

        zipname = self.error_fd.name
        if len(str(self.zfile_name)) > 0:
            zipname = self.xmldir / f'{self.zfile_name}.zip'

        return rcnt, pers, str(zipname), errors
