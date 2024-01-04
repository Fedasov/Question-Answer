from django.contrib import admin
from app.models import Question, Profile, Tag, Answer, LikeQuestion, LikeAnswer

admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(LikeQuestion)
admin.site.register(LikeAnswer)
