

select_count ='SELECT COUNT(*) FROM %s WHERE ist_fin=1'
"""
Имя	Тип	Размер
NUSL	NUMERIC	8
CARD	NUMERIC	8
FAM	CHAR	60
IMYA	CHAR	40
OTCH	CHAR	40
POL	CHAR	1
DATE_BIRTH	DATE	8
KATEG	NUMERIC	2
IST_FIN	NUMERIC	1
C_INSUR	CHAR	3
P_SER	CHAR	10
P_NUM	CHAR	20
FROM_FIRM	CHAR	3
PURP	NUMERIC	2
URGENT	NUMERIC	1
DATE_IN	DATE	8
DATE_OUT	DATE	8
Q_U	NUMERIC	1
RESULT_ILL	NUMERIC	1
CODE_MES	CHAR	10
RESULT_TRE	NUMERIC	1
DS_CLIN	CHAR	9
CHAR_MAIN	NUMERIC	1
VISIT_POL	NUMERIC	3
VISIT_HOM	NUMERIC	3
VISIT_DS	NUMERIC	3
VISIT_HS	NUMERIC	3
NSNDHOSP	CHAR	10
TYPE_HOSP	NUMERIC	1
SPECFIC	CHAR	3
DOCFIC	CHAR	3
TYPE_PAY	NUMERIC	1
D_TYPE	CHAR	3
K_PR	NUMERIC	1
VISIT_PR	NUMERIC	5
SMO	CHAR	5
NPR_MO	CHAR	6
PRVS	CHAR	9
IDDOKT	CHAR	16
VPOLIS	NUMERIC	1
NOVOR	CHAR	9
OS_SLUCH	NUMERIC	1
PROFIL	NUMERIC	3
DET	NUMERIC	1
VIDPOM	NUMERIC	4
USL_OK	NUMERIC	2
ISHOD	NUMERIC	3
RSLT	NUMERIC	3
DOCTYPE	NUMERIC	2
DOCSER	CHAR	10
DOCNUM	CHAR	20
SNILS	CHAR	14
UR_MO	CHAR	6
OKATO_OMS	CHAR	5
VNOV_D	NUMERIC	4
FOR_POM	NUMERIC	1
DS2	CHAR	10
DS3	CHAR	10
VNOV_M	NUMERIC	4
CODE_MES2	CHAR	7
DOST	NUMERIC	1
FAM_P	CHAR	40
IM_P	CHAR	40
OT_P	CHAR	40
W_P	NUMERIC	1
DR_P	DATE	8
DOST_P	NUMERIC	1
MR	CHAR	100
I_TYPE	NUMERIC	3
"""

get_hpm_data="""
SELECT 
    nusl AS idcase,
    nusl AS n_zap,
    nusl AS nhistory,
    date_in as date_z_1,
    date_out as date_z_2,
    date_in as date_1,
    date_out as date_2,
    card,
    
    vnov_d as mek, -- as pr_nov,
    
    purp,
    usl_ok,
    for_pom,
    rslt,
    ishod,
    vidpom,
    
    visit_pol, 
    visit_hom,
    
    date_in as npr_date,
    npr_mo,
    npr_mo as cons_mo,
    -- tal.hosp_mo,
    ds3 as naprlech,
    nsndhosp,
    type_hosp,
    d_type,
    
    ds_clin as ds1,
    ds2,
    char_main as c_zab,
    
    prvs,
    profil,
    snils as iddokt,
    
    vnov_m as idsp,
    
-- PACIENT
    smo,
    vpolis,
    p_num as npolis,
    p_num as id_pac,
    p_ser as spolis,
    okato_oms as smo_ok,

    fam, 
    imya as im,
    otch as ot,
    pol,
    date_birth as dr,
    dost,
    doctype,
    docser,
    docnum,
    -- crd.dul_date as docdate,
    -- crd.dul_org as docorg,
    -- crd.mo_att
        
FROM %s WHERE ist_fin=1;
"""

get_usl = """
SELECT
    usl.date_usl,
    usl.code_usl, 
    usl.kol_usl, 
    usl.exec_spec as spec, 
    usl.exec_doc as doc,
    usl.exec_podr as podr,
    tal.npr_mo,
    tal.npr_spec,
    tar.tarif as sumv_usl
FROM
    para_clin_%s as usl, 
    talonz_clin_%s as tal,
    tarifs_pmu_vzaimoras as tar
WHERE
    tal.tal_num = usl.tal_num AND
    tar.code = usl.code_usl AND
    tal.tal_num=%s
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