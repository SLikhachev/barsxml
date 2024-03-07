""" Test the SqlProvider class for Postgresql """


def test_db(db):
    """ test __init__ the SqlProvider class"""

    # test common
    assert db.schema == 'webz'
    assert db.cuser == 'postgres'
    assert db.table_exists('mo_local')
    assert db.table_exists('male_name')

    # test some states props filled with init session
    assert len(db.mo_local) > 10
    assert len(db.male_names) > 10
    assert len(db.usl) == 5
    assert len(db.spec_usl) > 10

    #print([name for name in db.male_names if name.startswith('сер')])

    # test get all records (talon_type = 1.2)
    hpm = db.get_hpm_data(False)
    assert len(hpm) == 5

    # test get fresh (talon_type=1)
    hpm = db.get_hpm_data(True)
    assert len(hpm) == 4

    # test get_npr_mo
    npr_mo = db.get_npr_mo({'from_firm': 337})
    assert npr_mo == int('250337')

    # test get gender
    male = db.get_pacient_gender({'im': 'СЕРГЕЙ'})
    female = db.get_pacient_gender({'im': 'ИРИНА'})
    undef = db.get_pacient_gender({'im': 'Авдотий'})
    assert (male == 'male') and (female == 'female') and (undef == 'female')

    # test get the pmus for the idcase
    usl = db.get_pmu_usl(4)
    assert len(usl) == 1
    assert usl[0]['date_usl'].isoformat() == '2024-03-04' and \
        usl[0]['code_usl'] == 'A05.30.004.002'

    # test get spec usl by the profil
    assert db.spec_usl.get(78, None) # -- рентгенология
    assert not db.spec_usl.get(63, None) # -- unknown profil