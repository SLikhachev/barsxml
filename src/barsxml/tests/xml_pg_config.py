""" test config """

import os
from barsxml.path.thispath import Path
from barsxml.config.postgresxml import *


SQL_SRV = dict(
    port=os.getenv('DB_PORT') or 5432,
    host=os.getenv('DB_HOST') or '127.0.0.1',
    dbname = os.getenv('DB_NAME') or 'hokuto',
    user=os.getenv('DB_USER') or 'postgres',
    password=os.getenv('DB_PASSWORD') or 'boruh',
    schema=os.getenv('DB_SCHEMA') or 'public',
    dbauth=os.getenv('DB_AUTH') or None
)

tests_dir = Path.script_dir()
MO_CODE = "250796"
PACK= os.getenv('TEST_PAC') or "app"
YEAR = os.getenv('TEST_YEAR') or "2021"
MONTH = os.getenv('TEST_MONTH') or "11"
BASE_XML_DIR = tests_dir / 'data' / SQL_SRV['dbname']

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
