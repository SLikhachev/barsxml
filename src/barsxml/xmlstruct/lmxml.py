
from types import SimpleNamespace as SN

LmStruct = SN(
    ZGLV = ('ZGLV', (
        'version',
        'data',
        'filename',
        'filename1'
    )),

    PERS = ('PERS', (
        'id_pac',
        'fam',
        'im',
        'ot',
        'w',
        'dr',
        'dost',
        'tel',
        'fam_p',
        'im_p',
        'ot_p',
        'w_p',
        'dr_p',
        'dost_p',
        'mr',
        'doctype',
        'docser',
        'docnum',
        'docdate',
        'docorg',
        'snils',
        'okatog',
        'okatop',
        'commentp'
    )),

    REQUIRED=(),
    IGNORED=('mr', 'snils', 'okatog', 'okatop', 'commentp'),
    CONST={'version':'3.2'},
    COUNTABLE={}
)
