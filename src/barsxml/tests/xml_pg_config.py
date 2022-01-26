
from barsxml.path.thispath import Path
from barsxml.config.postgresxml import *

SQL_SRV = dict(
    host='192.168.1.31',
    dbname = 'hokuto',
    user = 'postgres',
    password = 'boruh'
)

tests_dir = Path.script_dir()
MO_CODE = "250796"
YEAR="2021"
BASE_XML_DIR = tests_dir / 'data' / 'hokuto' 

DS = dict(
    p_per = 1,
    podr = 971,
    profil_k= 71
)

KSG = dict(
    ver_ksg = "2021",
    ksg_pg = 1,
    koef_z = 1,
    koef_up = 1,
    bztsz =  13308.72,
    koef_d = 1.369,
    koef_u = 0.8,
    sl_k = 0,
)
