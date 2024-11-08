from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    def __str__(self):
        return self.user.username

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
        # return self.order_by('likes_count')
        return self.all()
        #по умолчанию добавил сортировку в Answer в классе Meta
    def newest(self):
        return self.order_by('-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='questions')
    #при удалении профиля автора, сам вопрос не удаляется, просто поля автора переходит в NULL
    likes_count = models.IntegerField(default=0)
    answers_number = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.id})

    objects = QuestionManager()
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['likes_count']),
        ]
        #вместо этого можно использовать db_index=True в likes_count

        ordering = ['-created_at']

class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='answers')
    likes_count = models.IntegerField(default=0)

    objects = AnswerManager()
    def __str__(self):
        return f"{self.author}'s answer"
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['likes_count']),
        ]
        # вместо этого можно использовать db_index=True в likes_count

        ordering = ['-likes_count']

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
