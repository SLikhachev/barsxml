""" Bars MIS reporter class definition """

# NO reason as for time consumption
#from concurrent.futures import ThreadPoolExecutor, as_completed
#from functools import reduce
from typing import Tuple
from barsxml.sql import get_sql_provider
from barsxml.xmlproc.configx import ConfigAttrs
from barsxml.xmlproc.xmlwriter import XmlWriter
from barsxml.xmlproc.datadict import DataDict
from .reporter import XmlReport


class BarsXml(XmlReport):
    """ Bars container for report """

    __slots__ = ('cfg', 'data_dict', 'sql', 'xml_writer')

    def __init__(self, config: object, pack_type: str, mo_code: str, month: str, pack_num: int):
        """
            @params: config: object(
                SQL_PROVIDER=self.sql_provider, # String
                SQL_SRV=self.sql_srv, # dict
                YEAR = args['month'][0], #String
                BASE_XML_DIR=self.catalog('BASE_XML_DIR'),)
            @param: pack_type string of key for TYPES dict('type': int)
            @param: mo_code - code of MO '250799'
            @param: month - pack month '01'-'12'
            @param: pack_num - sequential pack number
        """
        # sanityze and init Configs
        self.cfg = ConfigAttrs(config, pack_type, mo_code, month, pack_num)

        # init UserDict
        self.data_dict = DataDict(mo_code=mo_code)

        # init SQL adapter dependency
        self.sql = get_sql_provider(config).SqlProvider(self.cfg)

        # init XML writer object
        self.xml_writer = XmlWriter(self.cfg)


    def make_xml(self, mark_sent: bool, get_fresh: bool, check=False) -> Tuple[int, int, str, int]:
        """ main class method
            @param: mark_sent: bool if TRUE set records field talon_type = 2 else ignore
            @param: get_fresh: bool if TRUE ignore already sent else get all records
            @param: check: bool if TRUE -> check tables recs only, don't make xml pack
        """

        self.xml_writer.init_files(check)
        self.sql.get_all_usp()
        self.sql.get_all_usl()
        rdata = self.sql.get_hpm_data(get_fresh)

        # total records, errors
        rcnt, errors = 0, 0
        for rdata_row in rdata:
            self.data_dict.next_rec(self.sql.rec_to_dict(rdata_row))
            idcase, card = rdata_row.idcase, rdata_row.card
            nmo = self.sql.get_npr_mo(self.data_dict)  # -> int
            try:
                self.data_dict.data_check(nmo)
                self.data_dict.set_usl(
                    self.sql.get_pmu_usl(idcase),
                    self.sql.get_spec_usl(rdata_row.profil)
                )
                self.data_dict.set_ksg(self.sql.get_ksg_data())
                self.xml_writer.write_data(self.data_dict)
                rcnt += 1
                # break
            except Exception as err:
                # print(rdata_row)
                # print(self.sql.spec_usl)
                #raise err
                # write error to the file
                self.xml_writer.write_error(f'{idcase}-{err}\n')
                self.sql.set_error(idcase, card, str(err))
                errors += 1
                continue

            # mark as sent
            if not check and mark_sent:
                self.sql.mark_as_sent(idcase)

        # end loop of all data
        # make ZIP archive
        if rcnt > 0 and not check:
            self.xml_writer.make_zip(rcnt)

        self.sql.close()
        return self.xml_writer.close(rcnt, len(self.data_dict.pers), errors)
