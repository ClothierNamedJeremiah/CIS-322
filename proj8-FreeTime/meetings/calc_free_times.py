import arrow
import timeblocks

def get_time_blocks(busy_blocks,begin_date,end_date,begin_time,end_time):
	"""
	@brief      Calculates a list of TimeBlocks (Free and Busy)

	@param      busy_blocks(list of TimeBlock Objects)  The list of busy times
    @param      begin_date (str): beginning date of date range. ISO formated date EX. 2017-11-15T00:00:00-08:00
    @param      end_date (str): ending day of date range. ISO formated date EX. 2017-11-21T00:00:00-08:00
    @param      begin_time (str): beginning time of time range. Format HH:mm EX. 08:00
    @param      end_time (str): ending time of time range. Format HH:mm EX. 17:00

	@return     A List of TimeBlocks (free and busy sorted in ascending order)
	"""
	# Setup arrow objects for time and date range
	begin_hr, begin_min = list(map(int,begin_time.split(":")))
	end_hr, end_min = list(map(int,end_time.split(":")))
	open_time = arrow.get(begin_date).replace(hour=begin_hr,minute=begin_min)
	open_year, open_month, open_day = list(map(int,open_time.format("YYYY:MM:DD").split(":")))
	end_time = arrow.get(end_date).replace(hour=end_hr,minute=end_min)
	
	# consolidate and trim the list of busy_blocks
	consolidated = consolidate(busy_blocks)
	trimmed = trim_blocks(consolidated,open_time,end_time)

	# add free TimeBlocks
	pointer = open_time
	current_day_start = open_time
	current_day_end = end_time.replace(year=open_year,month=open_month,day=open_day)
	times = [] # blocked times
	for block in trimmed:
		# Case: our pointer is at the end of a day's time range
		if pointer == current_day_end:
			current_day_start = current_day_start.shift(days=+1)
			current_day_end = current_day_end.shift(days=+1)
			pointer = current_day_start
		if pointer.time == block.get_start_time():
			pointer.time == block.get_end_time()
		# Pointer and current event are on same day
		if int(pointer.format("DD")) == int(block.get_start_time().format("DD")):
			free_block = timeblocks.TimeBlock(pointer,block.get_start_time())
			pointer = block.get_end_time()
			times.append(free_block)
		# Idea: stall going onto next block unitl pointer reaches current block_end and has filled that space with free time blocks
		else:
			fill_gaps(pointer,current_day_start,current_day_end,block,times)
			pointer = block.get_end_time()
			y,m,d = list(map(int,pointer.format("YYYY:MM:DD").split(":")))
			current_day_start = current_day_start.replace(year=y,month=m,day=d)
			current_day_end = current_day_end.replace(year=y,month=m,day=d)

		times.append(block)
	# If the last Event ends before the window closes, make the rest free TimeBlocks
	if pointer != end_time:
		fill_gaps(pointer,current_day_start,current_day_end,timeblocks.TimeBlock(end_time,None),times)
	return times



def fill_gaps(current_time, current_day_start, current_day_end, next_block, blocks):
	"""
	@brief      fills the range r for current_times < r < next_block.start_time

	@param      current_time(arrow): the end_time of the last placed TimeBlock
	@param      current_day_start(arrow): the start_time of a day within our date/time range
	@param      current_day_end(arrow): the end_time of a day within our date/time range
	@param      next_block(TimeBlock): The next busy block we will encounter
	@param 		blocks(list): list of TimeBlock Objects

	@return     None, updates the list 'blocks' by adding free TimeBlock Objects
	"""
	next_day = int(next_block.get_start_time().format("DD"))
	while int(current_time.format("DD")) != next_day:
		free_block = timeblocks.TimeBlock(current_time,current_day_end)
		if current_time != current_day_end:
			blocks.append(free_block)
		current_day_start = current_day_start.shift(days=+1)
		current_day_end = current_day_end.shift(days=+1)
		current_time = current_day_start


	# Fill our the rest of the days time with a free block
	if current_time != next_block.get_start_time():
		free_block = timeblocks.TimeBlock(current_time,next_block.get_start_time())
		blocks.append(free_block)

	return None


def consolidate(busy_blocks):
	"""
	@brief      consolidates the list of TimeBlocks

	@param      busy_blocks: list of TimeBlock Objects, representing busy times

	@return     a list of busy_blocks where overlapping TimeBlocks have been merged together
	"""
	consolidated = []
	prev = None
	for block in busy_blocks:
		if prev == None:
			prev = block
		# Case: There is a 'gap' between when the last block ended and the current starts
		elif prev.get_end_time() < block.get_start_time():
			consolidated.append(prev)
			prev = block
		# Case: There is some overlap between the two blocks
		else:
			description = prev.merge_descriptions(block)
			greater_end = max(prev.get_end_time(),block.get_end_time())
			block = timeblocks.TimeBlock(prev.get_start_time(),greater_end,description)
		prev = block
	consolidated.append(prev)

	return consolidated

def trim_blocks(busy_blocks,open_time,close_time):
	"""
	@brief      Trims a list of TimeBlocks so that they properly fit the time bounds

	@param      busy_blocks(list)  A list of TimeBlocks that represent busy_times
	@param      open_time (arrow)  The open date for our (date/time) range EX. 2017-11-15T08:15:00-08:00
	@param      close_time (arrow) The close date for our (date/time) range EX. 2017-11-17T15:30:00-08:00

	@return     a list of TimeBlocks, each trimmed to fit the bounds of time range.
	"""
	trimmed_blocks = []
	day_slices = create_daily_slices(open_time,close_time)
	for block in busy_blocks:
		event_slices = create_daily_slices(block.get_start_time(),block.get_end_time())
		trim = trim_day(block,day_slices,event_slices)
		trimmed_blocks += trim

	return trimmed_blocks

def trim_day(event_block,day_slices,event_slices):
	"""
	@brief      Trims a TimeBlock so that it properly fits the time and date range

	@param      event_block(TimeBlock)  A TimeBlock object
	@param      day_slices (list):  created by the function "create_daily_slices"

	@return     a list of TimeBlocks, each trimmed to fit the bounds of time range.

				For Example. A timeblock from 8:00 am - 4:00 pm would be trimmed down to
				9:00am - 3:00pm when the given timerange is 9:00am-3:00pm. Addittionally, one
				event that spans over multiple days will be split into separate time blocks. One for each day
	"""
	trimmed_blocks = []
	day_start = day_slices[0]
	event_start = event_slices[0]
	l = 0
	r = 0
	while day_start.format("YYYY/MM/DD") != event_start.format("YYYY/MM/DD"):
		if day_start < event_start:
			l += 1
			day_start = day_start.shift(days=+1)
		else:
			r += 1
			event_start = event_start.shift(days=+1)
	l *= 2
	r *= 2

	while l < len(day_slices) and r < len(event_slices):
		day_start = day_slices[l]
		day_end = day_slices[l+1]
		event_start = event_slices[r]
		event_end = event_slices[r+1]
		# The event_block will lay within no more of our slices
		if day_start > event_end:
			break
		# The event starts before and ends after our date/time range, just add the whole date/time range
		elif event_start <= day_start and event_end >= day_end:
			trimmed_blocks.append(timeblocks.TimeBlock(day_start,day_end,event_block.get_description()))
		# The event is completely within our slice
		elif day_start <= event_start and day_end >= event_end:
			trimmed_blocks.append(timeblocks.TimeBlock(event_start,event_end,event_block.get_description()))
			# break
		elif (event_start <= day_start) and (event_end <= day_end) and (event_end >= day_start):
			trimmed_blocks.append(timeblocks.TimeBlock(day_start,event_end,event_block.get_description()))
			# break
		elif day_start <= event_start and event_end >= day_end and event_start <= day_end:
			trimmed_blocks.append(timeblocks.TimeBlock(event_start, day_end, event_block.get_description()))
		l += 2
		r += 2

	return trimmed_blocks

def create_daily_slices(open_time,close_time):
 	"""
 	@brief		Creates a list of daily time ranges

	@param      open_time(arrow): The open date for our (date/time) range
	@param      close_time (arrow): The close date for our (date/time) range

	@returns    a list of arrow time slices for each day's range.
				For example, with an open time of 10/15/2017 8:00 AM and a close time of 10/21/2017 11:00 AM, we would list of the following:
				[10/15/2017 8:00 AM, 10/15/2017 11:00 AM, 10/16/2017 8:00 AM, 10/16/2017 11:00 AM,...,10/21/2017 8:00 AM, 10/21/2017 11:00 AM]
				stored individually as arrow objects
 	"""
 	open_year, open_month, open_day = list(map(int,open_time.format("YYYY:MM:DD").split(":")))
 	close_year, close_month, close_day = list(map(int,close_time.format("YYYY:MM:DD").split(":")))

 	starts = []
 	open_end = open_time.replace(year=close_year,month=close_month,day=close_day)
 	for r in arrow.Arrow.range('day',open_time,open_end):
 		starts.append(r)

 	ends = []
 	start_close = close_time.replace(year=open_year,month=open_month,day=open_day)
 	for r in arrow.Arrow.range('day',start_close,close_time):
 		ends.append(r)

 	slices = []
 	for i in range(len(starts)):
 		slices.append(starts[i])
 		slices.append(ends[i])

 	return slices
