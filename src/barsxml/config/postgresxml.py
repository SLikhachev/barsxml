""" settings for Posgresql DB native connection with psycopg2 """

SQL_PROVIDER = "postgres"

TEST_TABLE_EXISTS='''
SELECT EXISTS (
    SELECT FROM
        pg_tables
    WHERE
        schemaname = '{}' AND
        tablename  = '{}'
    );
'''

# names of the talons, paraclinic tables
TALONZ_CLIN='talonz_clin_'
PARA_CLIN='para_clin_'

# current schema and role for authorized access
SET_SCHEMA= "SET SCHEMA '%s';"
SET_ROLE="SET ROLE '%s';"

# Claim pg server's session variable

# Stmnt for PG >= v14
#SET_CUSER = "SET SESSION request.jwt.claims = '{"role": "webuser", "user": "jmoreva"}'"

# Stmnt for PG < v14
SET_CUSER='SET SESSION "request.jwt.claim.user" = %s;'

MALE_NAME = 'male_name'
GET_MALE_NAMES = 'SELECT name FROM male_name;'

MO_LOCAL = 'mo_local'


#127.0.0.1:7000/rpc/get_hpm_data?tbl=talonz_clin_21&mont=4&fresh=0
GET_HPM_DATA = 'SELECT * FROM get_hpm_data({talon_tbl}, {int_month}, {get_fresh})'
GET_ALL_LOCAL_MO = 'SELECT * FROM get_mo_local'
GET_ALL_USL= 'SELECT * FROM get_pmu_usl(%s, %s, %s)'
GET_SPEC_USL = 'SELECT * FROM get_spec_usl'

MARK_AS_SENT = "UPDATE talonz_clin_%s SET talon_type=2 WHERE tal_num=%s"

SET_ERROR = "INSERT INTO error_pack(tal_num, crd_num, error, cuser) VALUES ( %s, %s, %s, %s );"

#TRUNCATE_ERRORS = "TRUNCATE TABLE error_pack;"
ERRORS_TABLE_NAME = 'error_pack'
TRUNCATE_ERRORS = "DELETE FROM %s WHERE true"

GET_HPM_BY_MO = """
SELECT
    tal.tal_num AS idcase, --int
    tal.tal_num AS n_zap,
    tal.tal_num AS nhistory,
    tal.open_date as date_z_1,
    tal.close_date as date_z_2,
    tal.open_date as date_1,
    tal.close_date as date_2,
    tal.crd_num as card,

    tal.mek,

    tal.smo as tal_smo,
    tal.polis_type,
    tal.polis_ser,
    tal.polis_num,
    tal.smo_okato,

    tal.doc_spec as specfic,

    tal.purp,
    tal.usl_ok,
    tal.for_pom,
    tal.rslt,
    tal.ishod,

    tal.visit_pol,
    tal.visit_home as visit_hom,

    tal.npr_date,
    tal.npr_mo as from_firm, --int
    tal.naprlech,
    tal.nsndhosp,
    tal.d_type,
    tal.ds1,
    tal.ds2,
    tal.char1 as c_zab,

    spec.prvs,
    spec.profil,
    doc.snils as iddokt,

-- PACIENT
    crd.smo as smo,
    crd.polis_type as vpolis,
    crd.polis_num as npolis,
    crd.polis_num as id_pac,
    crd.polis_ser as spolis,
    crd.st_okato,
    crd.smo_ogrn,
    crd.smo_okato as smo_ok,
    crd.smo_name as smo_nam,
    crd.fam,
    crd.im,
    crd.ot,
    crd.gender as pol,
    crd.birth_date as dr,
    crd.dost as dost,
    crd.dul_type as doctype,
    crd.dul_serial as docser,
    crd.dul_number as docnum,
    crd.dul_date as docdate,
    crd.dul_org as docorg,
    crd.mo_att,
    crd.soc,
    crd.vz
FROM
    {talon_tbl} as tal,
    cardz_clin as crd,
    spec_prvs_profil as spec,
    doctor as doc
WHERE
    spec.spec=tal.doc_spec AND
    doc.spec=tal.doc_spec AND
    doc.code=tal.doc_code AND
    crd.crd_num=tal.crd_num AND
    tal.talon_type {fresh} AND
    tal.talon_month={int_month} AND
    tal.npr_mo={npr_mo}
ORDER BY tal.tal_num;
"""