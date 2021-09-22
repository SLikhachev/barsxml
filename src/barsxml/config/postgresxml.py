
SQL = "postgres"

#127.0.0.1:7000/rpc/get_hpm_data?tbl=talonz_clin_21&mont=4&fresh=0
GET_HPM_DATA = 'SELECT * FROM get_hpm_data(%s, %s, %s)'
GET_ALL_LOCAL_MO = 'SELECT * FROM get_mo_local'
GET_ALL_USL= 'SELECT * FROM get_pmu_usl(%s, %s, %s)'
GET_SPEC_USL = 'SELECT * FROM get_spec_usl'

MARK_AS_SENT = "UPDATE talonz_clin_%s SET talon_type=2 WHERE tal_num=%s"

SET_ERROR = "INSERT INTO error_pack(tal_num, crd_num, error) VALUES ( %s, %s, %s );"

TRUNCATE_ERRORS = "TRUNCATE TABLE error_pack;"