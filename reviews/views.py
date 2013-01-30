# Create your views here.

@login_required
def vote(request):
	if request.method == 'POST':
		v = Vote(
			feedback=Feedback(id=request.POST['feedback']),
			voted_by=CustomUser(id=request.user.id),
			type=VoteType(id=request.POST['vote_type'])
		)
	else:
		raise Http404