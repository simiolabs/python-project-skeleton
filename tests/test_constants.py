from nose.tools import *
from utilities_calc_cr.constantsCNFL import *

def test_get_time_segment():
    assert_equal(get_time_segment('07:00'), OFF_PEAK_TIME)
    assert_equal(get_time_segment('11:00'), PEAK_TIME)
    assert_equal(get_time_segment('12:00'), PEAK_TIME)
    assert_equal(get_time_segment('15:00'), OFF_PEAK_TIME)
    assert_equal(get_time_segment('18:00'), PEAK_TIME)
    assert_equal(get_time_segment('21:00'), NIGHT_TIME)
    assert_equal(get_time_segment('02:00'), NIGHT_TIME)

def test_get_consumption_segment_trr():
    assert_equal(get_consumption_segment_trr(50), TRR_LOW)
    assert_equal(get_consumption_segment_trr(400), TRR_MID)
    assert_equal(get_consumption_segment_trr(1000), TRR_HIGH)

def test_get_consumption_segment_tr():
    assert_equal(get_consumption_segment_tr(20), RR_FIXED)
    assert_equal(get_consumption_segment_tr(100), RR_LOW)
    assert_equal(get_consumption_segment_tr(250), RR_MID)
    assert_equal(get_consumption_segment_tr(350), RR_HIGH)

def test_get_consumption_segment_pr():
    assert_equal(get_consumption_segment_pr(5, PR_ENERGY), PR_E_LOW)
    assert_equal(get_consumption_segment_pr(200, PR_ENERGY), PR_MID)
    assert_equal(get_consumption_segment_pr(5000, PR_ENERGY), PR_E_HIGH)
    assert_equal(get_consumption_segment_pr(5, PR_POWER), PR_P_LOW)
    assert_equal(get_consumption_segment_pr(200, PR_POWER), PR_MID)
    assert_equal(get_consumption_segment_pr(5000, PR_POWER), PR_P_HIGH)
