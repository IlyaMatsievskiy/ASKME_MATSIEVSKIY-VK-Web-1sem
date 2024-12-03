import random
import time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The fill ratio for the data')

    def handle(self, *args, **options):
        ratio = options['ratio']
        time_now = time.time()
        print("Начало генерации")
        profiles = self.create_users(ratio)
        print(f'Генерация профилей и юзеров закончилась на {(time.time() - time_now) / 60} минуте')
        tags = self.create_tags(ratio)
        print(f'Генерация тегов закончилась на {(time.time() - time_now) / 60} минуте')
        questions = self.create_questions(ratio * 10, tags, profiles)
        print(f'Генерация вопросов закончилась на {(time.time() - time_now) / 60} минуте')
        answers = self.create_answers(ratio * 100, questions, profiles)
        print(f'Генерация ответов закончилась на {(time.time() - time_now) / 60} минуте')
        self.create_question_likes(ratio * 100, questions, profiles)
        print(f'Генерация лайков вопросов закончилась на {(time.time() - time_now) / 60} минуте')
        self.create_answer_likes(ratio * 100, answers, profiles)
        print(f'Генерация лайков ответов закончилась на {(time.time() - time_now) / 60} минуте')
        print("Генерация завершена!")

    def create_users(self, ratio):
        users = []
        profiles = []
        for i in range(ratio):
            user = User(
                username=f'user{i+1}',
                email=f'user{i}@mail.ru')
            user.set_password('testpassword')
            users.append(user)
            profiles.append(Profile(user=user))
        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)
        return profiles

    def create_tags(self, ratio):
        tags = []
        for i in range(ratio):
            tag = Tag(name=f'Tag{i+1}')
            tags.append(tag)
        Tag.objects.bulk_create(tags)
        return tags

    def create_questions(self, ratio, tags, profiles):
        questions = []
        for i in range(ratio):
            ind_pr = random.randint(1, len(profiles) - 1)
            question = Question(
                title=f'Question {i+1}',
                content=f'Content for question {i+1}',
                author=profiles[ind_pr],
                answers_number=0,
                likes_count=0
            )
            questions.append(question)
        Question.objects.bulk_create(questions)
        for question in questions:
            # можно написать add, если хотим только добавлять к существующим
            question.tags.set(random.sample(list(tags), k=min(3, len(tags))))
        return questions

    def create_answers(self, ratio, questions, profiles):
        answers = []
        for i in range(ratio):
            ind_que = random.randint(0, len(questions) - 1)
            ind_prof = random.randint(0, len(profiles) - 1)
            answer = Answer(
                content=f'Answer {i+1}',
                question=questions[ind_que],
                author=profiles[ind_prof],
                likes_count=0
            )
            answers.append(answer)
            questions[ind_que].answers_number += 1
        Answer.objects.bulk_create(answers)
        Question.objects.bulk_update(questions, ['answers_number'])
        return answers

    def create_question_likes(self, ratio, questions, profiles):
        likes = []
        num_questions = len(questions)
        num_profiles = len(profiles)

        existing_likes = set()

        for i in range(ratio):
            ind_que = i % num_questions
            ind_user = (i + 5) % num_profiles
            question = questions[ind_que]
            user = profiles[ind_user]

            if (question.id, user.id) not in existing_likes:
                existing_likes.add((question.id, user.id))
                likes.append(QuestionLike(question=question, user=user))
                questions[ind_que].likes_count += 1

        QuestionLike.objects.bulk_create(likes)
        Question.objects.bulk_update(questions, ['likes_count'])

    def create_answer_likes(self, ratio, answers, profiles):
        likes = []
        num_answers = len(answers)
        num_profiles = len(profiles)

        existing_likes = set()

        for i in range(ratio):
            ind_ans = i % num_answers
            ind_user = i % num_profiles
            answer = answers[ind_ans]
            user = profiles[ind_user]

            if (answer.id, user.id) not in existing_likes:
                existing_likes.add((answer.id, user.id))
                likes.append(AnswerLike(answer=answer, user=user))
                answers[ind_ans].likes_count += 1

        AnswerLike.objects.bulk_create(likes)
        print("Start")
        Answer.objects.bulk_update(answers, ['likes_count'])
        print("ВСЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕ")

