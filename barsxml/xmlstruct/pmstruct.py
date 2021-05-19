
from barsxml.xmlprod.utils import RowObject
from barsxml.xmlmix.maketags import MakeTags
from barsxml.xmlstruct.hdrstruct import HdrData


def pmData(data):
    # here we set additional attrs
    # type_pay
    # 1 - invoice
    # 2 - by soul
    if not data.get("type_pay", False):
        data["type_pay"] = 1
    return data


class PmUsl(RowObject):

    def __init__(self, mo, data):
        super().__init__(data)
        self.mo = mo


# posechenue obraschenie
class PmUsp(RowObject):

    def __init__(self, mo, data):
        super().__init__(data)
        self.mo = mo


class PmHdr(HdrData):

    def __init__(self, mo, year, month, typ, pack, sd_z=None, summ=None):
        super().__init__(mo, year, month, typ, pack)
        self.filename = self.p_file
        self.filename1 = self.h_file
        self.zglv_tags = (
            'data',
            'filename',
            'filename1',
        )
        self.zglv = ('ZGLV', self.zglv_tags)
        self.schet_tags = (
            'year',
            'month',
            'code_mo',
            'lpu'
        )
        self.schet = ('SCHET', self.schet_tags)


class PmSluch(MakeTags):

    def __init__(self, mo):
        super().__init__(mo)
        self.usl = None
        self.stom = None
        self.sl_id = 1
        
        self.usl_tags = (
            'idserv',
            # 'executor',  # self.executor # del as 495 paper
            # 'ex_spec',  # self.ex_spec # del as 495 paper
            #'rl'  # ignore
        )
        self.stom_tags = (
            'idstom',
            'code_usl',
            'zub',
            'kol_viz',
            'uet_fakt'
        )
        self.sluch_tags = (
            # 'SL',
            'sl_id',  # self..sl_id
            'idcase',  # tal.tal_num
            'card',  # tal.crd_num
            'from_firm',  # tal.npr_mo
            'purp',  # tal.purp
            'visit_pol',  # tal.vsit_pol
            'visit_hom',  # tal.visit_home
            'nsndhosp',  # tal.nsndhosp
            # 'specfic',  # tal.doc_spec # del as 495 paper
            'type_pay',  # self.type_pay
            'd_type',  # tal.d_type
            'naprlech',  # tal.naprlech
            ('usl', self.usl_tags, 'list'),
            ('stom', self.stom_tags, 'list')
        )
        self.sluch = (('SL', self.sluch_tags))

        self.ignore = (
            # 'stom',
            'rl'
        )
        # dummy counted tags
        self.cnt = (
            'idserv',
            'idstom',
        )
        self.required = (

        )

    def set_usl(self, tag, usl_list, usp):

        if not isinstance(usl_list, list):
            _u = [usl_list]
        else:
            _u = usl_list
        u_list = [PmUsl(self.mo, u) for u in _u]

        # as for 495 paper disabled
        '''
        if len(u_list) == 0:  # no PMU
            ex_spec = None
        else:
            # last ex_spec if any
            ex_spec = getattr(u_list[-1], 'ex_spec', None)
        '''

        # append posesh obrasch codes
        if bool(usp):
            u_list.append(PmUsp(self.mo, usp))
        
        setattr(self, tag, u_list)
        return self

    def get_sluch(self, data):
        return self.make_el(self.sluch, data)
