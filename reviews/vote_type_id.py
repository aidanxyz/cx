vote_types = {
	'weight': {
		1: 1,
		-1: 2
	},
	'name': {
		'agree': 1, 
		'disagree': 2
	}
}

def by_weight(weight):
	return vote_types['weight'][weight]

def by_name(name):
	return vote_types['name'][name]