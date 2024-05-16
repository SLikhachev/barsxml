""" XmlWRiter class definition """

import os
import shutil
from typing import Tuple
from time import time
from pathlib import Path
from tempfile import SpooledTemporaryFile as tmpf
#from tempfile import TemporaryFile as tmpf
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET
from barsxml.xmlmix.maketags import XmlTreeMaker
from barsxml.xmlstruct.hmxml import HmStruct as hmNS
from barsxml.xmlstruct.pmxml import PmStruct as pmNS
from barsxml.xmlstruct.lmxml import LmStruct as lmNS
from barsxml.xmlproc.configx import ConfigAttrs
from barsxml.xmlproc.hdrdict import make_hdr_dict
from barsxml.xmlproc.hdrdict import make_hm_hdr, make_pm_hdr, make_lm_hdr
from barsxml.xmlproc.datadict import DataDict
from barsxml.xmlproc.xmlsigner import XmlSigner


class XmlWriter:
    """ calss XmlWriter
        writes xml files successively HM -> PM -> LM from one data record
        then from next data record, no concurrency or muliprocrssing applied
    """

    #namespaces
    Ns = ('hm', 'pm', 'lm')

    # main xml root node for each NS
    NsTags = (hmNS.ZAP, pmNS.SLUCH, lmNS.PERS)

    # namespaces for file headers
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

        # init tree maker
        self.xml = XmlTreeMaker(cfg.mo_code, cfg.short_mo)

        error_file_name = cfg.xmldir / \
            f"errors_{cfg.pack_type}{str(time())[10:14]}.txt"
        self.error_fd = open(error_file_name, "w", encoding='utf-8')

    def init_files(self, check: bool):
        """ opens tmp files for report write """
        self.check = check
        if check:
            return

        # list of 3 tmp files descriptors
        self.ns_files = [tmpf(mode="r+", encoding="1251") for _ in self.Ns]

    def write_error(self, error: str):
        """ write error """
        self.error_fd.write(error)

    def write_hdr_body(self, tmpdir: TemporaryDirectory, hdr_ns: str):
        """ hdr body to file """
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
            ).write(hdr_file,
                xml_declaration=False,
                method='xml',
                encoding="unicode")
            hdr_file.write('\n')

            if hasattr(cns, 'SCHET'):
                ET.ElementTree(
                    self.xml.make_tree(hdr_ns, cns.SCHET, self.hdr)
                ).write(hdr_file,
                    xml_declaration=False,
                    method='xml',
                    encoding="unicode")
                hdr_file.write('\n')

            # flush tmp file body
            body_file = self.ns_files[ns_idx]
            body_file.seek(0)
            for line in body_file:
                #print(line)
                hdr_file.write(line)
            body_file.close()
            hdr_file.write(self.hdr["end_tag"])
            hdr_file.close()

        return _fname

    def write_data(self, data: DataDict):
        """ main data records to temp files """
        #add person to set
        pers = data.get_pers()
        if self.check:
            return  # no IO required
        for idx, cns in enumerate(self.Ns):
            if cns == 'lm' and pers is None:
                continue
            file = self.ns_files[idx]
            ET.ElementTree(
                # make tree with root node from current namespace
                self.xml.make_tree(cns, self.NsTags[idx], data)
            ).write(file,
                xml_declaration=False,
                method='xml',
                encoding="unicode")
            file.write('\n')

    def make_zip(self, rcnt: int, sign: bool = False):
        """ make zip file anyway and return it """
        with TemporaryDirectory() as tmpdir:

            self.hdr = make_hdr_dict(self.cfg, sd_z=rcnt, summ='0.00')
            to_zip = [self.write_hdr_body(tmpdir, cns) for cns in self.Ns]
            # print(to_zip)
            assert len(to_zip) == 3, f"Ошибка формирования файлов {to_zip}"

            # make sig files in sign is required
            if sign:
                signer = XmlSigner(self.cfg, tmpdir)
                _signed = [signer.sign_xml(file) for file in to_zip]
                assert len(_signed) == 3, f"Ошибка подписания файлов {_signed}"

            self.zfile_name = self.hdr["pack_name"].split('.')[0]

            os.chdir(str(self.xmldir))
            base_name = Path(self.xmldir) / self.zfile_name
            #print(self.xmldir, tmpdir, base_name)

            shutil.make_archive(str(base_name), 'zip', tmpdir)

    def close(self, rcnt: int, pers: int, errors: int) -> Tuple[int, int, str, int]:
        """ close openened files """

        output_file = self.error_fd.name
        if not self.error_fd.closed:
            self.error_fd.close()

        if errors == 0:
            os.remove(self.error_fd.name)
            output_file=''

        # close file anyway
        for file in self.ns_files:
            if not file.closed:
                file.close()

        # if zip had been write then return zip
        # else errors file or empty string
        if len(str(self.zfile_name)) > 0:
            output_file = self.xmldir / f'{self.zfile_name}.zip'

        # total HM records, LM records, ZIP name, errors find
        return rcnt, pers, str(output_file), errors
