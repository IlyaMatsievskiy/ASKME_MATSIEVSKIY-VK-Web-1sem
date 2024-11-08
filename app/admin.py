from django.contrib import admin
from app import models

# Register your models here.
# admin.site.register(models.Profile)
# admin.site.register(models.Tag)
# admin.site.register(models.Question)
# admin.site.register(models.Answer)
# admin.site.register(models.QuestionLike)
# admin.site.register(models.AnswerLike)

from django.contrib import admin
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author', 'likes_count', 'answers_number')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'author', 'question', 'likes_count')

@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('question', 'user')

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user')


