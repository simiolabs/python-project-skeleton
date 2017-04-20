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
