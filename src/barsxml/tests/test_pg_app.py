

import importlib
from datetime import datetime
from barsxml.xmlprod.barsxml import BarsXml

def test_app():
    time1 = datetime.now()
    config =  importlib.import_module(f'barsxml.tests.xml_pg_config')
    xml = BarsXml(config, "app", "04", "01")
    rc, pc, zname, errors = xml.make_xml(False, False, False)
    log = f"APP rc={rc}  pc={pc}  zname={zname}, errors={errors}"
    print(log)
    time2 = datetime.now()
    print(' Processing time %s sec' % (time2 - time1).seconds)