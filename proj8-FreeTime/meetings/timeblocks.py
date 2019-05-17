import arrow

class TimeBlock:

	def __init__(self,start_time,end_time,description=None):
		"""
		@brief      Constructs a TimeBlock

		@param      self:         		A Timeblock represents a "busy" or "free" timerange on a Google Calendar
		@param      start_time(arrow): 	The Time when the block starts
		@param      end_time(arrow): 	The Time when the block ends
		@param      description(str):  	The description of a timeblock's calendar event.
										The description will be  None is the timeblock is a "Free" timeblock
		"""
		self.start_time = start_time
		self.end_time = end_time
		self.description = description

	def __repr__(self):
		return "Description: {0}  |  Start Time: {1}  |  End Time: {2}".format(self.description,self.start_time,self.end_time)

	def __eq__(self,other):
		if other == None:
			return False
		return self.description == other.description and self.start_time == other.start_time and self.end_time == other.end_time

	def get_description(self):
		return self.description

	def get_start_time(self):
		return self.start_time

	def get_end_time(self):
		return self.end_time

	def set_start_time(self,start_time):
		self.start_time = start_time
	
	def set_end_time(self,end_time):
		self.end_time = end_time

	def set_description(self,description):
		self.description = description

	def is_within(self,other):
		"""
		@brief      Checks if two TimeBlocks' intervals overlap
		
		@param      self   The TimeBlock
		@param      other  The other TimeBlock
		
		@return     True if TimeBlocks overlap, False otherwise.
		"""
		# Case : Block1 ends before Block2 starts or Block2 ends before Block Starts
		if self.end_time < other.start_time or other.end_time < self.start_time:
			return False
		return True

	def get_overlap(self,other):
		"""
		@brief      Find the overlapping block shared between two TimeBlocks.
					Precondition: is_within(self,other) must be true for this function to work properly
		
		@param      self   The TimeBlock
		@param      other  The other TimeBlock
		
		@return     a Timeblock which represents the overlapping times shared between two TimeBlocks
		"""

		description = self.merge_descriptions(other)

		# Determine the Region which overlaps
		# Case 1: Block2 starts before Block1
		if other.start_time < self.start_time:
			# Case 1a: Block1 ends after Block2
			if self.end_time > other.end_time:
				overlap = TimeBlock(self.start_time,other.end_time,description)
			# Case 1b: Block1 ends before Block2
			else:
				overlap = TimeBlock(self.start_time,self.end_time,description)
		# Case 2: Block1 starts before Block2
		else:
			# Case 2a: Block1 ends after Block2
			if self.end_time > other.end_time:
				overlap = TimeBlock(other.start_time,other.end_time,description)
			# Case 2b: Block1 ends before Block2
			else:
				overlap = TimeBlock(other.start_time,self.end_time,description)

		return overlap
	
	def merge_descriptions(self,other):
		"""
		@brief      Merges two descriptions into one
		
		@param      self   The TimeBlock Object
		@param      other  The other TimeBlock Object
		
		@return     a description for both timeblocks
		"""
		if self.description and other.description:
			descr = self.description + ", " + other.description
		elif self.description:
			descr = self.description
		elif other.description:
			descr = other.description
		else:
			descr = None

		return descr


	def append_block(self,other):
		"""
		@brief      Creates a Timeblock by adding two events which follow each other
		            Precondition: self.end_time == other.start_time
		
		@param      self   The TimeBlock Object
		@param      other  The other TimeBlock Object
		
		@return     a Timeblock, which spans from the start time of 'self' to the end time of 'other'
		"""
		description = self.merge_descriptions(other)
		new_block = TimeBlock(self.start_time,other.end_time,description)
		return new_block