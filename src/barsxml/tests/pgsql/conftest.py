""" test config """

import os
from dataclasses import dataclass
import pytest

#from barsxml.path.thispath import Path
#from barsxml.config.postgresxml import *
from barsxml.sql.sqlpostgres import SqlProvider

@dataclass
class Config:
    sql_srv: dict
    ye_ar: str
    int_month: int

# The simple case where the Row-Level-Security not applied
@pytest.fixture
def config():
    year = os.getenv('TEST_YEAR') or '2023'
    return Config(
        {
            'port': os.getenv('DB_PORT') or 5432,
            'host': os.getenv('DB_HOST') or '127.0.0.1',
            'dbname': os.getenv('DB_NAME') or '',
            'user': os.getenv('DB_USER') or 'postgres',
            'password': os.getenv('DB_PASSWORD') or '',
            'schema': os.getenv('DB_SCHEMA') or 'public',
            'dbauth': os.getenv('DB_AUTH') or None,
        },
        year[2:],
        int(os.getenv('TEST_MONTH'))
    )

@pytest.fixture
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


"""
#POSTGRES=sql_srv
#SQL_PROVIDER= 'postgres'

#tests_dir = Path.script_dir()
#MO_CODE = "250796"
#PACK= os.getenv('TEST_PAC') or "app"
#year = os.getenv('TEST_YEAR') or "2021"
#MONTH = os.getenv('TEST_MONTH') or "11"
#base_xml_dir = tests_dir / 'data' / sql_srv['dbname']

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