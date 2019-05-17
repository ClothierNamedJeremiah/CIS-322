"""
Nose tests for acp_times.py
"""
from acp_times import open_time, close_time
import nose # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


def test_start():
	assert open_time(0,300,"1999-11-01T23:59:00+00:00") == "1999-11-01T23:59:00+00:00"
	assert close_time(0,300,"1999-11-01T23:59:00+00:00") == "1999-11-02T00:59:00+00:00"

# Tests Overall time limits as described in Article 9 on https://rusa.org/pages/rulesForRiders
def test_finish():
	assert close_time(200,200,"2017-01-01T00:00+00:00") == "2017-01-01T13:30:00+00:00"
	assert close_time(425,400,"2016-11-28T13:00+00:00") == "2016-11-29T16:00:00+00:00"

def test_out_of_accepted_range():
	assert close_time(1101,1000,"2000-05-10T05:00+00:00") == None
	assert close_time(1100,1000,"2000-05-10T05:00+00:00") == "2000-05-13T08:00:00+00:00"

def test_before_and_after():
	assert open_time(599,600,"2007-08-10T08:51+00:00") == "2007-08-11T03:37:00+00:00"
	assert close_time(599,600,"2007-08-10T08:51+00:00") == "2007-08-12T00:47:00+00:00"

	assert open_time(601,600,"2007-08-10T08:51+00:00") == "2007-08-11T03:39:00+00:00"
	assert close_time(601,600,"2007-08-10T08:51+00:00") == "2007-08-12T00:51:00+00:00"