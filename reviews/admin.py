from reviews.models import Feedback, Vote, VoteType, Detail
from django.contrib import admin

admin.site.register(Feedback)
admin.site.register(Vote)
admin.site.register(VoteType)
admin.site.register(Detail)
