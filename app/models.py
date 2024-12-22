import os

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.contrib.auth.models import User
from django.template.context_processors import request
from django.urls import reverse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVectorField, SearchVector


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # При удалении пользователя удалится и профиль
    nickname = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.nickname or self.user.username

    def save(self, *args, **kwargs):
        # Проверяем, существует ли объект и есть ли старая аватарка
        if self.pk:
            old_avatar = Profile.objects.filter(pk=self.pk).first().avatar
            if old_avatar and self.avatar != old_avatar:  # Если аватарка меняется
                old_avatar_path = os.path.join(settings.MEDIA_ROOT, old_avatar.name)
                if os.path.isfile(old_avatar_path):  # Удаляем только физически существующий файл
                    os.remove(old_avatar_path)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаляем аватарку при удалении профиля
        if self.avatar:
            avatar_path = os.path.join(settings.MEDIA_ROOT, self.avatar.name)
            if os.path.isfile(avatar_path):
                os.remove(avatar_path)

        super().delete(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def best(self):
        return self.order_by('-answers_number')
    def newest(self):
        # return self.order_by('-created_at')
        return self.all()
    # по умолчанию добавил сортировку в Question в классе Meta
    def filter_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name) #в классе тег ищутся теги с подходящим именем

class AnswerManager(models.Manager):
    def best(self):
        # return self.order_by('-is_correct', '-likes_count')
        return self.all()
        #по умолчанию добавил сортировку в Answer в классе Meta
    def newest(self):
        return self.order_by('-is_correct', '-created_at') #сначала верные


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='questions')
    #при удалении профиля автора, сам вопрос не удаляется, просто поля автора переходит в NULL
    likes_count = models.IntegerField(default=0)
    answers_number = models.IntegerField(default=0)
    search_vector = SearchVectorField(null=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.id})

    objects = QuestionManager()
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['likes_count']),
            GinIndex(fields=['search_vector']),
        ]
        #вместо этого можно использовать db_index=True в likes_count

        ordering = ['-created_at']

class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='answers')
    likes_count = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()
    def __str__(self):
        return f"{self.author}'s answer"
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['likes_count']),
        ]
        # вместо этого можно использовать db_index=True в likes_count

        ordering = ['-is_correct', '-likes_count'] #сначала будут показываться все верные, а потом уже по лайкам

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_likes')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    #можно было сделать SET_NULL, но тогда можно создать ботов и накрутить лайки
    class Meta:
        unique_together = ('question', 'user')
    def save(self, *args, **kwargs):
        if not self.pk:  #проверка на наличие первичного ключа, если нет, значит только что лайкнули
            self.question.likes_count += 1
            self.question.save() #сохранили инфу о лайке в вопрос
        super().save(*args, **kwargs) #сохранили в questionlike
    def delete(self, *args, **kwargs):
        if self.question.likes_count > 0:
            self.question.likes_count -= 1
        self.question.save()
        super().delete(*args, **kwargs)

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_likes')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    #можно было сделать SET_NULL, но тогда можно создать ботов и накрутить лайки
    class Meta:
        unique_together = ('answer', 'user')
    def save(self, *args, **kwargs):
        if not self.pk:  #проверка на наличие первичного ключа, если нет, значит только что лайкнули
            self.answer.likes_count += 1
            self.answer.save() #сохранили инфу о лайке в вопрос
        super().save(*args, **kwargs) #сохранили в questionlike
    def delete(self, *args, **kwargs):
        if self.answer.likes_count > 0:
            self.answer.likes_count -= 1
        self.answer.save()
        super().delete(*args, **kwargs)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if not hasattr(instance, 'profile'): #если еще не создан
#             Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


@receiver(post_save, sender=Answer)
def increment_answer_count(sender, instance, created, **kwargs):
    if created:
        instance.question.answers_number += 1
        instance.question.save()

@receiver(post_delete, sender=Answer)
def decrement_answer_count(sender, instance, **kwargs):
    if instance.question.answers_number > 0:
        instance.question.answers_number -= 1
        instance.question.save()


@receiver(post_save, sender=Question)
def update_search_vector(sender, instance, **kwargs):
    # Проверяем, если update_fields не передан или пустой, пропускаем
    if kwargs.get('update_fields') is None or 'search_vector' in kwargs.get('update_fields', []):
        return  # Избегаем повторного вызова для поля search_vector

    # Отключаем сигнал перед сохранением
    post_save.disconnect(update_search_vector, sender=Question)

    try:
        # Обновляем только search_vector
        instance.search_vector = SearchVector('title', 'text')  # Используйте нужные поля
        instance.save(update_fields=['search_vector'])
    finally:
        # Включаем сигнал обратно
        post_save.connect(update_search_vector, sender=Question)

