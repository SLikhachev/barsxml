""" module """
SQL_PROVIDER = "postgres"


TALONZ_CLIN='talonz_clin_'
PARA_CLIN='para_clin_'

SET_SCHEMA= "SET SCHEMA '%s';"
SET_ROLE="SET ROLE '%s';"
# for PG >= v14
#SET_CUSER = "SET SESSION request.jwt.claims = '{"role": "webuser", "user": "jmoreva"}'"
SET_CUSER='SET SESSION "request.jwt.claim.user" = %s;'

#127.0.0.1:7000/rpc/get_hpm_data?tbl=talonz_clin_21&mont=4&fresh=0
GET_HPM_DATA = 'SELECT * FROM get_hpm_data(%s, %s, %s)'
GET_ALL_LOCAL_MO = 'SELECT * FROM get_mo_local'
GET_ALL_USL= 'SELECT * FROM get_pmu_usl(%s, %s, %s)'
GET_SPEC_USL = 'SELECT * FROM get_spec_usl'

MARK_AS_SENT = "UPDATE talonz_clin_%s SET talon_type=2 WHERE tal_num=%s"

SET_ERROR = "INSERT INTO error_pack(tal_num, crd_num, error, cuser) VALUES ( %s, %s, %s, %s );"

#TRUNCATE_ERRORS = "TRUNCATE TABLE error_pack;"
ERRORS_TABLE_NAME = 'error_pack'
TRUNCATE_ERRORS = "DELETE FROM %s WHERE true"
