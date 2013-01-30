from reviews.models import Feedback, ModerationReason, FeedbackCloseInfo, FeedbackEditInfo
from django.contrib import admin

admin.site.register(Feedback)
admin.site.register(ModerationReason)
admin.site.register(FeedbackCloseInfo)
admin.site.register(FeedbackEditInfo)