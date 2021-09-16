from django.contrib import admin

from .models import (
    Poll,
    Answer,
    UserAnswer,
    UserQuestionResponse,
    Question,
    UserPollResponse,
)


admin.site.register(Poll)
admin.site.register(Answer)
admin.site.register(UserAnswer)
admin.site.register(UserQuestionResponse)
admin.site.register(UserPollResponse)
admin.site.register(Question)
