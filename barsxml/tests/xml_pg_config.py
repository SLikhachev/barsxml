
from barsxml.path.thispath import Path
from barsxml.config.pgxml import *


DB_NAME = 'hokuto'
DB_USER = 'postgres'
DB_PASS = 'boruh'

DB_CONN = f"dbname={DB_NAME} user={DB_USER} password={DB_PASS}"

tests_dir = Path.script_dir()
MO_CODE = "796"
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
