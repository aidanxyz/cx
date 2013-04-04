class UserDidNotUseItem(Exception):
	def __init__(self, value="You didn't use this item"):
		self.value = value

class PriorityOutOfRange(Exception):
	def  __init__(self, value="Wrong priority value"):
		self.value = value

class MustAgreeFirst(Exception):
	def  __init__(self, value="Before setting priority you need to agree with feedback first"):
		self.value = value

class WrongOrderPriority(Exception):
	def  __init__(self, value="Wrong order or duplicate priority per feedbacks column"):
		self.value = value