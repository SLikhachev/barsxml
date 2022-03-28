

SQL_PROVIDER = "pgrest"

TALONZ_TBL = 'talonz_clin_'
PARA_TBL = 'para_clin_'
#127.0.0.1:7000/rpc/get_hpm_data?tbl=talonz_clin_21&mont=4&fresh=0
GET_HPM_DATA = '/rpc/get_hpm_data'
GET_ALL_LOCAL_MO = '/get_mo_local'
GET_ALL_USL= '/rpc/get_pmu_usl'
GET_SPEC_USL = '/get_spec_usl'

MARK_WHERE = f'?tal_num=eq.%s'
MARK_AS_SENT=dict(talon_type=2)

SET_ERROR = "INSERT INTO error_pack(tal_num, crd_num, error) VALUES ( %s, %s, %s );"
