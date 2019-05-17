"""
Nose tests for calc_free_times.py
Run using 'nosetests' in the meetings directory
"""
import nose
import timeblocks
import calc_free_times
import arrow

def test_consolidate():
	block1 = timeblocks.TimeBlock(arrow.get("2017-11-07T07:00:00-08:00"),arrow.get("2017-11-07T10:15:00-08:00"), "Block 1")
	block2 = timeblocks.TimeBlock(arrow.get("2017-11-07T10:15:00-08:00"),arrow.get("2017-11-07T13:45:00-08:00"), "Block 2")
	block3 = timeblocks.TimeBlock(arrow.get("2017-11-07T10:30:00-08:00"),arrow.get("2017-11-07T11:30:00-08:00"), "Block 3")

	block4 = timeblocks.TimeBlock(arrow.get("2017-11-08T08:30:00-08:00"),arrow.get("2017-11-08T10:30:00-08:00"), "Block 4")
	block5 = timeblocks.TimeBlock(arrow.get("2017-11-08T09:30:00-08:00"),arrow.get("2017-11-08T12:00:00-08:00"))
	block6 = timeblocks.TimeBlock(arrow.get("2017-11-08T15:30:00-08:00"),arrow.get("2017-11-08T17:00:00-08:00"), "Block 6")

	block_list = [block1,block2,block3,block4,block5,block6]
	c_list = calc_free_times.consolidate(block_list)

	correct = [timeblocks.TimeBlock(arrow.get("2017-11-07T07:00:00-08:00"),arrow.get("2017-11-07T13:45:00-08:00"), "Block 1, Block 2, Block 3"),
				timeblocks.TimeBlock(arrow.get("2017-11-08T08:30:00-08:00"),arrow.get("2017-11-08T12:00:00-08:00"),"Block 4"),
				timeblocks.TimeBlock(arrow.get("2017-11-08T15:30:00-08:00"),arrow.get("2017-11-08T17:00:00-08:00"), "Block 6")]

	assert(correct == c_list)



	assert(calc_free_times)

def test_daily_slices():
	timerange_open = arrow.get("2017-10-15T08:00:00-08:00")
	timerange_close = arrow.get("2017-10-17T11:00:00-08:00")
	slices = calc_free_times.create_daily_slices(timerange_open,timerange_close)
	correct = [arrow.get("2017-10-15T08:00:00-08:00"),arrow.get("2017-10-15T11:00:00-08:00"),
				arrow.get("2017-10-16T08:00:00-08:00"),arrow.get("2017-10-16T11:00:00-08:00"),
				arrow.get("2017-10-17T08:00:00-08:00"),arrow.get("2017-10-17T11:00:00-08:00")]
	assert(slices == correct)

	timerange_open = arrow.get("2015-12-30T07:59:00-08:00")
	timerange_close = arrow.get("2016-01-02T15:27:00-08:00")
	slices = calc_free_times.create_daily_slices(timerange_open,timerange_close)
	correct = [arrow.get("2015-12-30T07:59:00-08:00"), arrow.get("2015-12-30T15:27:00-08:00"),
				arrow.get("2015-12-31T07:59:00-08:00"), arrow.get("2015-12-31T15:27:00-08:00"),
				arrow.get("2016-01-01T07:59:00-08:00"), arrow.get("2016-01-01T15:27:00-08:00"),
				arrow.get("2016-01-02T07:59:00-08:00"), arrow.get("2016-01-02T15:27:00-08:00")]
	assert(slices == correct)

def test_trim():
	### Test Cases for trim_day
	timerange_open = arrow.get("2017-10-08T08:20:00-08:00")
	timerange_close = arrow.get("2017-10-18T11:59:00-08:00")

	block = timeblocks.TimeBlock(arrow.get("2017-10-07T06:30:00-08:00"),arrow.get("2017-10-14T10:08:00-08:00"), "Away on Holiday")
	slices = calc_free_times.create_daily_slices(timerange_open,timerange_close)
	event_slices = calc_free_times.create_daily_slices(block.get_start_time(),block.get_end_time())
	trimmed = calc_free_times.trim_day(block,slices,event_slices)

	correct = [timeblocks.TimeBlock(arrow.get("2017-10-08T08:20:00-08:00"),arrow.get("2017-10-08T10:08:00-08:00"), "Away on Holiday"),
				timeblocks.TimeBlock(arrow.get("2017-10-09T08:20:00-08:00"),arrow.get("2017-10-09T10:08:00-08:00"), "Away on Holiday"),
				timeblocks.TimeBlock(arrow.get("2017-10-10T08:20:00-08:00"),arrow.get("2017-10-10T10:08:00-08:00"), "Away on Holiday"),
				timeblocks.TimeBlock(arrow.get("2017-10-11T08:20:00-08:00"),arrow.get("2017-10-11T10:08:00-08:00"), "Away on Holiday"),
				timeblocks.TimeBlock(arrow.get("2017-10-12T08:20:00-08:00"),arrow.get("2017-10-12T10:08:00-08:00"), "Away on Holiday"),
				timeblocks.TimeBlock(arrow.get("2017-10-13T08:20:00-08:00"),arrow.get("2017-10-13T10:08:00-08:00"), "Away on Holiday"),
				timeblocks.TimeBlock(arrow.get("2017-10-14T08:20:00-08:00"),arrow.get("2017-10-14T10:08:00-08:00"), "Away on Holiday")
				]
	assert(trimmed == correct)

	block2 = timeblocks.TimeBlock(arrow.get("2017-10-14T05:30:00-08:00"),arrow.get("2017-10-14T20:15:00-08:00"), "Busy All Day")
	event_slices = calc_free_times.create_daily_slices(block2.get_start_time(),block2.get_end_time())
	trimmed = calc_free_times.trim_day(block2,slices,event_slices)

	correct = [timeblocks.TimeBlock(arrow.get("2017-10-14T08:20:00-08:00"),arrow.get("2017-10-14T11:59:00-08:00"),"Busy All Day")]
	assert(trimmed == correct)

	block3 = timeblocks.TimeBlock(arrow.get("2017-10-18T10:30:00-08:00"),arrow.get("2017-10-18T20:15:00-08:00"), "Busy 1/2 Day")
	event_slices = calc_free_times.create_daily_slices(block3.get_start_time(),block3.get_end_time())
	trimmed = calc_free_times.trim_day(block2,slices,event_slices)

	correct = [timeblocks.TimeBlock(arrow.get("2017-10-18T10:30:00-08:00"),arrow.get("2017-10-18T11:59:00-08:00"), "Busy 1/2 Day")]

	### Test case for trim_blocks
	timerange_open = arrow.get("2017-11-07T10:20:00-08:00")
	timerange_close = arrow.get("2017-11-11T15:59:00-08:00")

	blocks = [timeblocks.TimeBlock(arrow.get("2017-11-07T07:00:00-08:00"),arrow.get("2017-11-07T13:45:00-08:00"), "Block 1, Block 2, Block 3"),
				timeblocks.TimeBlock(arrow.get("2017-11-10T15:30:00-08:00"),arrow.get("2017-11-12T17:00:00-08:00"), "Block 6")
			]

	trimmed = calc_free_times.trim_blocks(blocks,timerange_open,timerange_close)

	correct = [timeblocks.TimeBlock(arrow.get("2017-11-07T10:20:00-08:00"),arrow.get("2017-11-07T13:45:00-08:00"), "Block 1, Block 2, Block 3"),
				timeblocks.TimeBlock(arrow.get("2017-11-10T15:30:00-08:00"),arrow.get("2017-11-10T15:59:00-08:00"), "Block 6"),
				timeblocks.TimeBlock(arrow.get("2017-11-11T15:30:00-08:00"),arrow.get("2017-11-11T15:59:00-08:00"), "Block 6")
	]

	assert(trimmed == correct)

def test_free_times():
	begin_date = "2017-10-07T00:00:00-08:00"
	begin_time = "06:15"
	end_date = "2017-10-11T00:00:00-08:00"
	end_time = "15:59"

	busy_blocks = [timeblocks.TimeBlock(arrow.get("2017-10-08T08:20:00-08:00"),arrow.get("2017-10-08T10:00:00-08:00"), "B2"),
				timeblocks.TimeBlock(arrow.get("2017-10-09T06:15:00-08:00"),arrow.get("2017-10-09T15:59:00-08:00"), "B1"),
				timeblocks.TimeBlock(arrow.get("2017-10-10T13:55:00-08:00"),arrow.get("2017-10-10T15:59:00-08:00"), "B4")
				]
	blocks = calc_free_times.get_time_blocks(busy_blocks,begin_date,end_date,begin_time,end_time)

	correct = [timeblocks.TimeBlock(arrow.get("2017-10-07T06:15:00-08:00"),arrow.get("2017-10-07T15:59:00-08:00")),
				timeblocks.TimeBlock(arrow.get("2017-10-08T06:15:00-08:00"),arrow.get("2017-10-08T08:20:00-08:00")),
				timeblocks.TimeBlock(arrow.get("2017-10-08T08:20:00-08:00"),arrow.get("2017-10-08T10:00:00-08:00"),"B2"),
				timeblocks.TimeBlock(arrow.get("2017-10-08T10:00:00-08:00"),arrow.get("2017-10-08T15:59:00-08:00")),
				timeblocks.TimeBlock(arrow.get("2017-10-09T06:15:00-08:00"),arrow.get("2017-10-09T15:59:00-08:00"),"B1"),
				timeblocks.TimeBlock(arrow.get("2017-10-10T06:15:00-08:00"),arrow.get("2017-10-10T13:55:00-08:00")),
				timeblocks.TimeBlock(arrow.get("2017-10-10T13:55:00-08:00"),arrow.get("2017-10-10T15:59:00-08:00"),"B4"),
				timeblocks.TimeBlock(arrow.get("2017-10-11T06:15:00-08:00"),arrow.get("2017-10-11T15:59:00-08:00"))
				]
	assert(blocks == correct)