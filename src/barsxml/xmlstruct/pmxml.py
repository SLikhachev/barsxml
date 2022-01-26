

from types import SimpleNamespace as SN

PmStruct = SN(
    ZGLV = ('ZGLV', (
        'data',
        'filename',
        'filename1'
    )),

    SCHET = ('SCHET', (
        'year',
        'month',
        'code_mo',
        'lpu'
    )),

    SLUCH = ('SL', (
        'sl_id',  # self..sl_id
        'idcase',  # tal.tal_num
        'card',  # tal.crd_num
        'from_firm',  # tal.npr_mo
        'purp',  # tal.purp
        'visit_pol',  # tal.vsit_pol
        'visit_hom',  # tal.visit_home
        'nsndhosp',  # tal.nsndhosp
        'type_pay',  # self.type_pay
        'd_type',  # tal.d_type
        'naprlech',  # tal.naprlech
        ('usl',  ('idserv',),)
    )),

    REQUIRED=('sl_id', 'idcase', 'card', 'purp', 'visit_pol', 'visit_hom', 'idserv' ),
    IGNORED=(),
    CONST={'sl_id': 1},
    COUNTABLE={'usl':'idserv'}
)
