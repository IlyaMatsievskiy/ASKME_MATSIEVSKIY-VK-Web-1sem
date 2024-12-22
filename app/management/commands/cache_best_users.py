from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from django.core.cache import cache
from django.db.models import Sum
from app.models import Profile, Question, Answer

class Command(BaseCommand):
    help = 'Обновляет кэш лучших пользователей'

    def handle(self, *args, **kwargs):
        cache_key = "best_users"
        one_week_ago = now() - timedelta(days=7)

        # Считаем рейтинг пользователей
        question_scores = (
            Question.objects.filter(created_at__gte=one_week_ago)
            .values('author')
            .annotate(score=Sum('likes_count'))
        )
        answer_scores = (
            Answer.objects.filter(created_at__gte=one_week_ago)
            .values('author')
            .annotate(score=Sum('likes_count'))
        )

        # Суммируем баллы от вопросов и ответов
        combined_scores = {}
        for entry in question_scores:
            combined_scores[entry['author']] = combined_scores.get(entry['author'], 0) + entry['score']
        for entry in answer_scores:
            combined_scores[entry['author']] = combined_scores.get(entry['author'], 0) + entry['score']

        # Сортируем и выбираем топ-10
        best_users = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        best_users_data = [{'id': user_id, 'score': score} for user_id, score in best_users]

        # Сохраняем в кэш
        cache.set(cache_key, best_users_data, 60 * 60 * 24)  # Кэшируем на 24 часа
        self.stdout.write(self.style.SUCCESS("Кэш лучших пользователей обновлен"))
