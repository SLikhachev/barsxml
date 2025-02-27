""" Test the utils/data_checker.py """

import pytest

def test_gender(db, data_dict):
    """ Test the gender check"""
    #print(rdata[0])
    get_fresh=False

    # read rows of data
    rdata = db.get_hpm_data(get_fresh)

    # make next record from 1st row
    data_dict.next_rec(db.rec_to_dict(rdata[0]))

    npolis = data_dict["npolis"]
    check=True
    data_dict.data_check(check, db)

    data_dict['im'] = 'ИРИНА'
    # the npolis key was deleted by the prev checker
    data_dict['npolis'] = npolis

    #print(data_dict)
    with pytest.raises(AssertionError, match=f"{data_dict["idcase"]}-Проверте пол пациента"):
        data_dict.data_check(check, db)


    # if check False then test must have been passed
    # prepare data_dict to the second test
    assert data_dict['im'] == 'ИРИНА' and data_dict["pol"] == 'м'

    data_dict['npolis'] = npolis
    del data_dict["gender"]
    check=False
    data_dict.data_check(check, db)
