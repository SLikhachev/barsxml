""" test """

import os
import importlib
from pathlib import Path
from datetime import datetime
from barsxml.xmlprod.barsxml import BarsXml

pytest_plugins= ("pytest_env",)

def test_app():
    """ test """
    time1 = datetime.now()
    config = importlib.import_module('barsxml.tests.xml_pg_config')

    path = config.tests_dir
    data_path = config.base_xml_dir / config.PACK
    print(f'test path: {data_path.parts}')
    for folder in data_path.parts[-3:]:
        path = path / folder
        if not Path.exists(path):
            Path.mkdir(path)

    sign_xml = os.getenv('SIGN_XML') or False
    limit =  os.getenv('RECS_LIMIT') or 0
    iimit = int(limit)

    xml = BarsXml(config, config.PACK, config.MO_CODE, config.MONTH, 1)
    _rc, _pc, zname, errors = xml.make_xml(limit, False, False, False, sign_xml)

    log = f"APP rc={_rc}  pc={_pc}  zname={zname}, errors={errors}"
    print(log)
    time2 = datetime.now()
    print(f'Processing time {(time2-time1).seconds} sec')
