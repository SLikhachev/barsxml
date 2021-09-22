
import requests
from barsxml.sql import get_sql_provider
from barsxml.tests import xml_pgrest_config as config


def test_sql_module_name():
    assert f"basexml.sql.sql{config.SQL}" == "basexml.sql.sqlpgrest"


def test_sql_class_init():
    sql = get_sql_provider(config).SqlProvider(config, '250796','2021', '04')
    assert sql.talon_tbl == f'{config.TALONZ_TBL}{sql.ye_ar}', 'Wrong talonz_clin name'
    assert sql.para_tbl == f'{config.PARA_TBL}{sql.ye_ar}', 'Wrong para_clin name'
    try:
        requests.options(f'{sql.db}/doctor', timeout=0.5)
    except requests.exceptions.Timeout as e:
        raise e


def test_get_local_mo():
    sql = get_sql_provider(config).SqlProvider(config, '250796','2021', '04')
    sql.get_local_mo()
    assert isinstance(sql.mo_local, dict), 'mo_local is not a dict'
    assert len(sql.mo_local) > 0, 'mo_local dict empty'
    assert sql.mo_local[int(sql.mo_code[3:])] == int(sql.mo_code), f'self code: {sql.mo_code} not found in mo_local'


def test_get_hpm_usl():
    sql = get_sql_provider(config).SqlProvider(config, '250796', '2021', '04')
    sql.get_local_mo()
    sql.get_all_usl()
    sql.get_all_usp()
    assert isinstance(sql.spec_usl, dict), 'spec_usl is not a dict'
    assert isinstance(sql.usl, dict), 'usl is not a dict'
    assert len(sql.spec_usl) > 0, 'spec_usl dict empty'
    assert len(sql.usl) > 0, 'usl dict empty'
    rdata = sql.get_hpm_data('xml', False)
    usl, npr, rc  = 0, 0, 0
    for d in rdata:
        rc += 1
        id = d['idcase']
        if len( sql.get_pmu_usl(id)) > 0:
            usl += 1
        assert len(sql.get_spec_usl(d)) > 0, f'idcase: {id} no spec usl found'
        if sql.get_npr_mo(d):
            npr += 1

    assert usl > 0, f'No one USL to Data attached'
    assert npr > 0, f'No one NPR MO in Data find'
    print(f'\nrecords {rc}\n')