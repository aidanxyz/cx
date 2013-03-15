class SelfVotingException(Exception):
	def __init__(self, value="You can't vote for feedback you created"):
		self.value = value

class UserDidNotUseItem(Exception):
	def __init__(self, value="You didn't use this item"):
		self.value = value

class PriorityOutOfRange(Exception):
	def  __init__(self, value="Wrong priority value"):
		self.value = value