

from barsxml.sql import get_sql_provider
from barsxml.tests import xml_dbf_config as config


def test_sql_module_name():
    assert f"basexml.sql.sql{config.SQL}" == "basexml.sql.sqldbf"

def test_sql_class_init():
    sql = get_sql_provider(config).SqlProvider(config, "2021", "03")
    assert sql.dbfn == "228103"
    print (f" DBF dir {sql.db_dir}")
    assert sql.rr == f"RR{sql.dbfn}.dbf"
    sql.close()

HPM = (
    ("idcase", "3699"),
    ("nhistory", "3699"),
    ("card", "80901"),
    ("fam", "Соловьева"),
    ("im", "Анфиса"),
    ("ot", "Полуэктовна"),
    ("pol", "ж"),
    ("dr", "1978-07-31"),
    ("npolis", "9076540856000421"),
    ("date_1", "2020-12-21"),
    ("date_2", "2020-12-30"),
    ("ds1", "J06.9"),
    ("smo", "25016"),
    ("prvs", "95"),
    ("iddokt", "101-220-211-47"),
    ("profil", "97"),
    ("vidpom", "12"),
    ("smo_ok", "05000"),
    ("naprlech", "654122568"),
    ("idsp", "33")
)

def test_get_hpm_npr_mo_usl():
    sql = get_sql_provider(config).SqlProvider(config, "2021", "03")
    rrs = sql.get_hpm_data('app', False)
    assert len(list(rrs)) == 4
    r1 = list(rrs)[0]
    for attr, val in HPM:
        rv = getattr(r1, attr)
        if isinstance(rv, float):
            rv = int(rv)
        assert str(rv) == val

    assert r1.npr_mo == "250228"
    sql.close()

RPS = (
("26", "101-220-211-47", "34", "B03.016.003"),
("26", "101-220-211-47", "34", "A09.05.010"),
("26", "101-220-211-47", "34", "A09.05.017"),
("26", "101-220-211-47", "34", "A09.05.020"),
("26", "101-220-211-47", "34", "A09.05.023"),
("26", "101-220-211-47", "34", "A09.05.041"),
("26", "101-220-211-47", "34", "A09.05.042"),
("26", "101-220-211-47", "34", "B03.016.006"),
("95", "101-220-211-47", "97", "B01.047.002")
)

class Data:
    idcase = 3699


def test_get_usl():
    sql = get_sql_provider(config).SqlProvider(config, "2021", "03")
    rps = sql.get_usl(Data)
    assert len(list(rps)) == 9
    row = 0
    for rp in rps:
        acnt = 0
        for attr in ("prvs", "code_md", "profil", "code_usl"):
            pv = getattr(rp, attr)
            if isinstance(pv, float):
                pv = int(pv)
            assert str(pv) == RPS[row][acnt]
            acnt += 1
        row += 1

    sql.close()
