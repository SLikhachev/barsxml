

from barsxml.path_class.thisPath import Path


#os.path.abspath(os.path.dirname(__file__))
SQL = "dbf" 
MO_CODE = "228"
RR_DIR = str(Path.script_dir()/'data')

COUNT_OMS ='SELECT COUNT(*) FROM %s WHERE ist_fin=1'
"""
NUSL	-- NUMERIC 8
CARD	-- NUMERIC 8
FAM	-- CHAR 60
IMYA	-- CHAR 40
OTCH	-- CHAR 40
POL	-- CHAR 1
DATE_BIRTH -- DATE 8
KATEG --NUMERIC 2
IST_FIN -- NUMERIC 1
C_INSUR -- CHAR 3
P_SER -- CHAR	10
P_NUM -- CHAR 20
FROM_FIRM -- CHAR3
PURP -- NUMERIC 2
URGENT -- NUMERIC	1
DATE_IN -- DATE 8
DATE_OUT -- DATE 8
Q_U -- NUMERIC	1
RESULT_ILL -- NUMERIC 1
CODE_MES -- CHAR 10
RESULT_TRE-- NUMERIC	1
DS_CLIN -- CHAR 9
CHAR_MAIN -- NUMERIC 1
VISIT_POL -- NUMERIC 3
VISIT_HOM -- NUMERIC 3
VISIT_DS -- NUMERIC 3
VISIT_HS -- NUMERIC 3
NSNDHOSP -- CHAR 10
TYPE_HOSP -- NUMERIC 1
SPECFIC -- CHAR 3
DOCFIC -- CHAR 3
TYPE_PAY -- NUMERIC 1
D_TYPE -- CHAR 3
K_PR -- NUMERIC 1
VISIT_PR -- NUMERIC 5
SMO -- CHAR 5
NPR_MO -- CHAR 6
PRVS -- CHAR 9
IDDOKT -- CHAR 16
VPOLIS NUMERIC 1
NOVOR -- CHAR 9
OS_SLUCH -- NUMERIC 1
PROFIL	NUMERIC	3
DET -- NUMERIC 1
VIDPOM -- NUMERIC 4
USL_OK -- NUMERIC 2
ISHOD -- NUMERIC 3
RSLT -- NUMERIC 3
DOCTYPE -- NUMERIC	2
DOCSER -- CHAR 10
DOCNUM -- CHAR 20
SNILS -- CHAR 14
UR_MO -- CHAR 6
OKATO_OMS -- CHAR 5
VNOV_D -- NUMERIC 4
FOR_POM -- NUMERIC	1
DS2 -- CHAR 10
DS3 -- CHAR 10
VNOV_M -- NUMERIC 4
CODE_MES2 -- CHAR 7
DOST -- NUMERIC 1
FAM_P -- CHAR 40
IM_P -- CHAR 40
OT_P -- CHAR 40
W_P -- NUMERIC 1
DR_P -- DATE 8
DOST_P -- NUMERIC 1
MR -- CHAR 100
I_TYPE -- NUMERIC 3
"""

GET_RRS="""
SELECT 
    nusl AS idcase,
    nusl AS n_zap,
    nusl AS nhistory,
    date_in AS date_z_1,
    date_out AS date_z_2,
    date_in AS date_1,
    date_out AS date_2,
    card,
    vnov_d AS mek, 
    
    purp,
    usl_ok,
    for_pom,
    rslt,
    ishod,
    vidpom,
    
    visit_pol, 
    visit_hom,
    
    date_in AS npr_date,
    npr_mo,
    npr_mo AS cons_mo,
    ds3 as naprlech,
    nsndhosp,
    type_hosp,
    d_type,
    
    ds_clin AS ds1,
    ds2,
    char_main AS c_zab,
    
    specfic,
    prvs,
    profil,
    iddokt,
    
    vnov_m AS idsp,
    
    smo,
    vpolis,
    p_num AS npolis,
    p_num AS id_pac,
    p_ser AS spolis,
    okato_oms AS smo_ok,

    fam, 
    imya AS im,
    otch AS ot,
    pol,
    date_birth AS dr,
    dost,
    doctype,
    docser,
    docnum
FROM %s WHERE ist_fin=1;
"""
"""
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
'prvs',
'code_md',
"""

GET_RPS = """
SELECT
    kol_usl, 
    prvs,
    profil,
    iddokt AS code_md,
    code_nom AS code_usl,
    281 AS podr,
    '0.00'AS sumv_usl
FROM %s WHERE nusl = ?
"""

get_spec_usl = """
SELECT
    tal.open_date as date_usl,
    prof.one_visit as code_usl1,
    prof.two_visit as code_usl2,
    1 as kol_usl, 
    prof.podr as podr, 
    tal.doc_spec as spec,
    tal.doc_code as doc
FROM
    talonz_clin_%s as tal, profil as prof, spec_prvs_profil as spp
WHERE 
    tal.doc_spec = spp.spec AND
    prof.id = spp.profil AND 
    tal.tal_num=%s
"""

get_stom = ''

set_error="INSERT INTO error_pack(tal_num, crd_num, error) VALUES ( %s, %s, %s );"

truncate_errors="TRUNCATE TABLE error_pack;"