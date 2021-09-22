

import importlib
from datetime import datetime
from barsxml.xmlprod.barsxml import BarsXml

def test_app():
    time1 = datetime.now()
    config =  importlib.import_module(f'barsxml.tests.xml_pgrest_config')
    xml = BarsXml(config, 'xml', '250796', '04', 1)
    rc, pc, zname, errors = xml.make_xml(False, False, False)
    log = f"APP rc={rc}  pc={pc}  zname={zname}, errors={errors}\n"
    print(log)
    time2 = datetime.now()
    print(' Processing time %s sec\n' % (time2 - time1).seconds)