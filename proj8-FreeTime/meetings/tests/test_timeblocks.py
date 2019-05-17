"""
Nose tests for timeblocks.py
Run using 'nosetests' in the meetings directory
"""
import nose
import timeblocks
import arrow

def test_get():
	block1 = timeblocks.TimeBlock(arrow.get("2017-11-07T14:00:00-08:00"),arrow.get("2017-11-07T15:00:00-08:00"), "Block 1")
	assert(block1.get_description() == "Block 1")
	assert(block1.get_start_time() == arrow.get("2017-11-07T14:00:00-08:00"))
	assert(block1.get_end_time() == arrow.get("2017-11-07T15:00:00-08:00"))

def test_within():
	block1 = timeblocks.TimeBlock(arrow.get("2017-11-07T12:00:00-08:00"),arrow.get("2017-11-07T15:00:00-08:00"), "Block 1")
	block2 = timeblocks.TimeBlock(arrow.get("2017-11-07T15:01:00-08:00"),arrow.get("2017-11-07T17:00:00-08:00"), "Block 2")
	block3 = timeblocks.TimeBlock(arrow.get("2017-11-07T11:00:00-08:00"),arrow.get("2017-11-07T16:00:00-08:00"), "Block 3")

	assert(block3.is_within(block2))
	assert(block3.is_within(block1))
	assert(not (block2.is_within(block1)))

def test_overlap():
	block1 = timeblocks.TimeBlock(arrow.get("2017-11-07T12:00:00-08:00"),arrow.get("2017-11-07T15:00:00-08:00"), "Block 1")
	block2 = timeblocks.TimeBlock(arrow.get("2017-11-07T10:00:00-08:00"),arrow.get("2017-11-07T12:01:00-08:00"), "Block 2")
	block3 = timeblocks.TimeBlock(arrow.get("2017-11-07T09:00:00-08:00"),arrow.get("2017-11-07T16:00:00-08:00"))
	block4 = timeblocks.TimeBlock(arrow.get("2017-11-07T15:00:00-08:00"),arrow.get("2017-11-07T23:00:00-08:00"))

	assert(block1.get_overlap(block2) == timeblocks.TimeBlock(arrow.get("2017-11-07T12:00:00-08:00"),
												arrow.get("2017-11-07T12:01:00-08:00"),
												"Block 1, Block 2"))

	assert(block2.get_overlap(block3) == timeblocks.TimeBlock(arrow.get("2017-11-07T10:00:00-08:00"),arrow.get("2017-11-07T12:01:00-08:00"),"Block 2"))
	assert(block4.get_overlap(block1) == timeblocks.TimeBlock(arrow.get("2017-11-07T15:00:00-08:00"),arrow.get("2017-11-07T15:00:00-08:00"),"Block 1"))

def test_append():
	block1 = timeblocks.TimeBlock(arrow.get("2017-11-07T12:00:00-08:00"),arrow.get("2017-11-07T15:00:00-08:00"), "Block 1")
	block2 = timeblocks.TimeBlock(arrow.get("2017-11-07T15:00:00-08:00"),arrow.get("2017-11-07T17:00:00-08:00"), "Block 2")
	assert(block1.append_block(block2) == timeblocks.TimeBlock(arrow.get("2017-11-07T12:00:00-08:00"),arrow.get("2017-11-07T17:00:00-08:00"),"Block 1, Block 2"))
