""" test config """

import os
from dataclasses import dataclass
import pytest

from barsxml.path.thispath import Path
#from barsxml.config.postgresxml import *
from barsxml.sql.sqlpostgres import SqlProvider
from barsxml.xmlproc.datadict import DataDict

""" Cofigutation parameters

POSTGRES=sql_srv
SQL_PROVIDER= 'postgres'

DS = dict(
    p_per=1,
    podr=971,
    profil_k=71
)

KSG = dict(
    ver_ksg="2021",
    ksg_pg=1,
    koef_z=1,
    koef_up=1,
    bztsz=13308.72,
    koef_d=1.369,
    koef_u=0.8,
    sl_k=0,
)

"""

@dataclass
class Config:
    sql_srv: dict
    year: str
    ye_ar: str
    month: str
    int_month: int
    mo_code: int
    pack_type: str
    tests_dir: str
    POSTGRES = None
    SQL_PROVIDER: str = 'postgres'
    base_xml_dir: str = ''

# The simple case where the Row-Level-Security not applied
@pytest.fixture(scope='session')
def config():
    year = os.getenv('TEST_YEAR') or '2023'
    month =  os.getenv('TEST_MONTH')
    cfg = Config(
        {
            'port': os.getenv('DB_PORT') or 5432,
            'host': os.getenv('DB_HOST') or '127.0.0.1',
            'dbname': os.getenv('DB_NAME') or '',
            'user': os.getenv('DB_USER') or 'postgres',
            'password': os.getenv('DB_PASSWORD') or '',
            'schema': os.getenv('DB_SCHEMA') or 'public',
            'dbauth': os.getenv('DB_AUTH') or None,
        },
        year,
        year[2:],
        month,
        int(month),
        os.getenv('MO_CODE'),
        os.getenv('PACK_TYPE'),
        Path.script_dir().parent
    )
    cfg.base_xml_dir = cfg.tests_dir / 'data' / cfg.sql_srv['dbname']
    cfg.POSTGRES = cfg.sql_srv
    return cfg

@pytest.fixture(scope='session')
def db(config):
    _dbc = SqlProvider(config)

    init_db_file = os.getenv('DB_INIT_FILE')

    with open(init_db_file, encoding='utf-8') as fd:
        _dbc.qurs.execute(f"SET search_path={config.sql_srv['schema']}")
        _sql = fd.read()
        _dbc.qurs.execute(_sql)
        _dbc._db.commit()

    yield _dbc
    _dbc.close()


#@pytest.fixture(scope='session')
#def rdata(db):
#    get_fresh=False
#    return db.get_hpm_data(get_fresh)


@pytest.fixture(scope='session')
def data_dict(config):
    return DataDict(config.mo_code)
