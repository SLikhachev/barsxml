""" test """

import importlib
from pathlib import Path
from datetime import datetime
from barsxml.xmlprod.barsxml import BarsXml

pytest_plugins= ("pytest_env",)

def test_app():
    """ test """
    time1 = datetime.now()
    config = importlib.import_module('barsxml.tests.xml_pg_config')

    if not Path.exists(config.BASE_XML_DIR):
        Path.mkdir(config.BASE_XML_DIR)

    pack = config.BASE_XML_DIR / config.PACK

    if not Path.exists(pack):
        Path.mkdir(pack)

    xml = BarsXml(config, config.PACK, config.MO_CODE, config.MONTH, 1)
    _rc, _pc, zname, errors = xml.make_xml(False, False, False)

    log = f"APP rc={_rc}  pc={_pc}  zname={zname}, errors={errors}"
    print(log)
    time2 = datetime.now()
    print(f'Processing time {(time2-time1).seconds} sec')
