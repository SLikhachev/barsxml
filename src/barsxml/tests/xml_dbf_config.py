
from barsxml.path.thispath import Path
from barsxml.config.dbfxml import *


tests_dir = Path.script_dir()
MO_CODE = "445"
YEAR="2021"
RR_DIR = str(tests_dir / 'data' / 'import')
BASE_XML_DIR = tests_dir / 'data' / 'export'

# PCR RECORD (DS1, SPECFIC)
PCR = dict(ds="J20.9", specfic="09", rslt=314)
# IFA RECORD (DS1, SPECFIC, RSLT)
IFA = dict(ds="Z01.7", specfic="09", rslt=315)

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
