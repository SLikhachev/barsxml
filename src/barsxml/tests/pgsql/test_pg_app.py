""" Test the main BarsXml's class method """

import os
from pathlib import Path
from datetime import datetime
import pytest

from barsxml.xmlprod.barsxml import BarsXml


@pytest.fixture(scope='module')
def xml(config):
    """ make class instance """

    path = config.tests_dir
    data_path = config.base_xml_dir / config.pack_type
    #print(f'test path: {data_path.parts}')
    for folder in data_path.parts[-3:]:
        path = path / folder
        if not Path.exists(path):
            Path.mkdir(path)
    pack_num = 1

    #def __init__(self, config: object, pack_type: str, mo_code: str, month: str, pack_num: int):
    _xml = BarsXml(config, config.pack_type, config.mo_code, config.month, pack_num)
    return _xml

@pytest.fixture(scope='module')
def db(config, xml):
    _dbc = xml.sql

    assert _dbc.schema == config.sql_srv['schema']
    assert _dbc.cuser == config.sql_srv['user']

    if config.init_db_file:
        with open(config.init_db_file, encoding='utf-8') as fd:
            _dbc.qurs.execute(f"SET search_path={xml.cfg.sql_srv['schema']}")
            _sql = fd.read()
            _dbc.qurs.execute(_sql)
            _dbc._db.commit()

    yield _dbc
    #_dbc.close()


def test_sql_class_init(db):
    """ test the SqlProvider class was initiaded properly """

    assert db.table_exists('mo_local')
    assert db.table_exists('male_name')

    # test some states props filled with init session
    assert len(db.mo_local) > 10
    assert len(db.male_names) > 10
    assert len(db.usl) > 0
    assert len(db.spec_usl) > 10


def test_make_method(config, xml):
    """ test the main method with the params from the pytest.ini file"""

    time1 = datetime.now()
    sign_xml = os.getenv('SIGN_XML') or False
    limit =  os.getenv('RECS_LIMIT') or 0
    check = os.getenv('CHECK_ONLY') or False
    mark_sent = os.getenv('MARK_SENT') or False
    get_fresh = os.getenv('GET_FRESH') or False

    limit = int(limit)
    print (f"""\nTEST CONFIG:
        limit={limit}, check={check},
        mark_sent={mark_sent}, get_fresh={get_fresh}""")

    _dbc = config.sql_srv
    try:
        #def make_xml(self,
        # limit: int, mark_sent: bool, get_fresh: bool, check=False, sign=False)
        # -> Tuple[int, int, str, int]:
        _rc, _pc, zname, errors = xml.make_xml(
            limit, mark_sent, get_fresh, check, sign_xml
        )

        log = f"""\nAPPLICATION:
          DB: {_dbc['dbname']}, SCHEMA: {_dbc['schema']}
          HPM_records={_rc}
          LM_records={_pc}
          ZIP_file_name={zname},
          found_errors={errors}
        """
        print(log)
        time2 = datetime.now()
        print(f'Processing time {(time2-time1).seconds} sec')
    except Exception as exc:
        print(f"The test make method exception: {exc}")
        raise exc
