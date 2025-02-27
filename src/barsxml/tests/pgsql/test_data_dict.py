""" Test the utils/data_dict.py
Test the DataDict class self calculated attributes

"""

#import pytest

def test_pcel_inokray(db, data_dict):
    """ Test pcel calculation """
    get_fresh=False

    # read rows of data
    rdata = db.get_hpm_data(get_fresh)

    # make dict next record from 1st row
    row_dict = db.rec_to_dict(rdata[0])
    # set inokray SMO_OK
    row_dict["smo_ok"] = "87024"
    # set DS1 as K87.1 in  ( A00-T99 )
    row_dict["ds1"] = "K87.1"

    # Calculate attrs DataDict
    data_dict.next_rec(row_dict)
    data_dict.hm_data_attrs()

    # assert p_cel == 1.3
    assert data_dict["p_cel"] == "1.3"

    # change data
    data_dict["ds1"] = "Z03.1"
    # recalculate data atts
    data_dict.hm_data_attrs()

    # assert p_cel == 1.3
    assert data_dict["p_cel"] == "2.6"
