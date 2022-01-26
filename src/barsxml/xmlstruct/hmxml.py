

from types import SimpleNamespace as SN

HmStruct = SN(
    ZGLV = ('ZGLV', (
        'version',
        'data',
        'filename',
        'sd_z',
    )),

    SCHET = ('SCHET', (
        'code',
        'code_mo',
        'year',
        'month',
        'nschet',
        'dschet',
        'summav',
    )),

    ZAP = ('ZAP', (

        'n_zap',  # tal.tal_num
        'pr_nov',  # self.pr_nov

        ('pacient', (
            'id_pac',  # tal.crd_num
            'vpolis',  # crd.polis_type || tal.polis_type
            'spolis',  # crd.polis_ser || tal.polis_ser
            'npolis',  # crd.polis_num || tal.polis_num
            'st_okato',  # crd.st_okato
            'smo',  # crd.smo || tal.smo
            #'smo_ogrn',  # crd.smo_ogrn
            #'smo_ok',  # crd.smo_okato || tal.smo_okato
            'enp', #crd.enp || tal.enp
            'smo_nam',  # crd.smo_name
            'inv',  # ignore
            'mse',  # ignore
            'novor',
            'vnov_d'  # ignore
        )),

        ('z_sl', (
            'idcase',  # tal.tal_num
            'usl_ok',  # tal.usl_ok
            'vidpom',  # vidpom
            'for_pom',  # in tal.for_pom only urgent if set
            'npr_mo',  # tal.npr_mo
            'npr_date',  # tal.npr_date
            'lpu',  # self.lpu
            'date_z_1',  # tal.open_date
            'date_z_2',  # tal.close_date
            'kd_z',  # = KD
            'vnov_m',  # ignore
            'rslt',  # tal.rslt
            'ishod',  # tal.ishod
            'os_sluch',  # self.os_sluch # d_type = 5 (os_sl= 2)
            'vb_p',  # ignore

            ('sl', (
                'sl_id',  # self
                'lpu_1',  # data.lpu_1 # ignore yet
                'podr',  # data.podr # ignore yet
                'profil',  # data.profil
                'profil_k',  # tal.prof_k
                'det',
                'p_cel',  # self.p_cel
                'nhistory',  # data.nhistory
                'p_per',  # DS 1
                'date_1',  # data.date_1
                'date_2',  # data.date_2
                'kd',  # DSTAC
                'ds0',  # ignore
                'ds1',  # data.ds1
                'ds2',  # data.ds2
                'c_zab',  # data.c_zab
                'dn',  #
                'code_mes1',  # ignore
                'code_mes2',  # ignore

                ('ksg_kpg', (
                    'n_ksg',
                    'ver_ksg',
                    'ksg_pg',
                    'n_kpg',
                    'koef_z',
                    'koef_up',
                    'bztsz',
                    'koef_d',
                    'koef_u',
                    'dkk1',
                    'dkk2',
                    'sl_k',
                    'it_sl',

                    ('sl_koef', (
                        'idsl',
                        'z_sl'
                    )),
                )),

                'reab',  # ignore
                'prvs',  # data.prvs
                'vers_spec',  # self
                'iddokt',  # data
                'ed_col',
                'tarif',  # ignore
                'sum_m',

                ('usl', (
                    'idserv',
                    'lpu',  # self.lpu
                    'lpu_1',  # ignore
                    'podr',  # ignore
                    'profil',
                    'vid_vme',
                    'det',
                    'date_in',
                    'date_out',
                    'ds',
                    'code_usl',
                    'kol_usl',
                    'tarif',
                    'sumv_usl',

                    ('mr_usl_n', (
                        'mr_n',
                        'prvs',
                        'code_md'
                    )),
                    'npl'  # ignore
                )),
            )),
            'idsp',  # self.idsp
            'sumv',  # self.sumv
        ))
    )),

    REQUIRED=(
        ## Zap
        'n_zap',
        'pr_nov',

        ## Pacient
        'id_pac',  # tal.crd_num
        'vpolis',  # crd.polis_type
        #'npolis',  # crd.polis_num
        'novor',

        ## Z_sl
        'idcase',
        'usl_ok',
        'vidpom',
        'for_pom',
        'lpu',
        'date_z_1',
        'date_z_2',
        'rslt',
        'ishod',
        'idsp',
        'sumv',

        ## Sl
        'sl_id',
        'profil',
        'det',
        'nhistory',
        'date_1',
        'date_2',
        'ds1',
        # 'c_zab',
        'prvs',
        'vers_spec',
        'iddokt',
        'sum_m',
    ),
    IGNORED=(
        ## Pacient
        'inv',
        'mse',
        'vnov_d',

        ## Z_sl
        #'kd_z', # tal. # just ignore yet
        'vnov_m',
        'vb_p',

        ## Sl
        'lpu_1', # data.lpu_1 # ignore yet
        # 'podr',  # data.podr # ignore yet

        ## Sl DS
        #'profil_k', # tal.prof_k # ignore yet
        #'p_per',  # DS later
        #'kd',  # DS
        #'dn',
        #'ksg_kpg',
        'code_mes1',
        'code_mes2',
        'reab',
        #'ed_col',
        'tarif',
    ),
    CONST={
        'version': '3.2',
        'sl_id': 1,
        'vers_spec': 'V021',
        'novor': 0
    },
    COUNTABLE={
        'usl':'idserv',
        'mr_usl_n':'mr_n'
    }
)
