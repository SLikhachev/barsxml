""" Test the utils/data_checker.py """

import pytest

'''
# as for H VERSION = 3.2 ENP tag
    _d["enp"] = _d["npolis"]
    del _d["npolis"]
'''


def test_data_check(db, data_dict):
    """ simple test to catch any error """

    data_dict.data_check(True, db)


def _test_gender(db, data_dict):
    """ Test the gender check"""

    npolis = data_dict["npolis"]
    data_dict['im'] = 'ИРИНА'
    data_dict["pol"] == 'ж'
    check=True

    #test must have been passed
    data_dict.data_check(check, db)

    data_dict["pol"] == 'м'
    # the npolis key was deleted by the prev checker
    data_dict['npolis'] = npolis

    #print(data_dict)
    with pytest.raises(AssertionError, match=f"{data_dict["idcase"]}-Проверте пол пациента"):
        data_dict.data_check(check, db)

    data_dict['npolis'] = npolis
    del data_dict["gender"]

    # if check False then test must have been passed
    check=False
    data_dict.data_check(check, db)


def _test_naprlech_len(db, data_dict):

    npolis = data_dict["npolis"]
    data_dict["naprlech"] = "123456789"
    check=True

    #test must have been passed
    data_dict.data_check(check, db)

    data_dict["naprlech"] = "1234567890123456"
    # the npolis key was deleted by the prev checker
    data_dict["npolis"] = npolis

    with pytest.raises(
            AssertionError,
            match=f"{data_dict['idcase']}-Номер направления слишком длинный"
        ):
        data_dict.data_check(check, db)
