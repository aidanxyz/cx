from reviews.models import Feedback, ModerationReason, FeedbackCloseInfo, FeedbackEditInfo, Vote, VoteType, Detail
from django.contrib import admin

admin.site.register(Feedback)
admin.site.register(ModerationReason)
admin.site.register(FeedbackCloseInfo)
admin.site.register(FeedbackEditInfo)
admin.site.register(Vote)
admin.site.register(VoteType)
admin.site.register(Detail)
