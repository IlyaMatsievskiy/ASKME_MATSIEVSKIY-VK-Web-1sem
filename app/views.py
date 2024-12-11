from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from .models import Answer, Question, Tag, Profile, QuestionLike, AnswerLike
from .forms import LoginForm, SignUpForm, SettingsForm, AskForm, AnswerForm

TAGS = Tag.objects.all()
MEMBERS = Profile.objects.all()
page_count = 10


def paginate(object_list, request, per_page=page_count):
    paginator = Paginator(object_list, per_page)
    page = request.GET.get('page', 1)
    try:
        return paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        return paginator.page(1)


# Create your views here.
def index(request):
    page_obj = paginate(Question.objects.all(), request)
    return render(request, template_name = 'index.html', context={'questions': page_obj, 'members': MEMBERS[0:5], 'tags': TAGS[0:5], 'page_obj': page_obj})


def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect(f"/login/?continue={request.path}")

        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.profile
            answer.question = question
            answer.save()
            answers_list = list(Answer.objects.filter(question=question))

            answer_index = answers_list.index(answer)

            page_number = (answer_index // page_count) + 1
            # Перенаправляем пользователя на нужную страницу с ответами
            return redirect(f"{reverse('question', args=[question_id])}?page={page_number}#{answer.id}") # комментарий к ошибке не выводим
    else:
        form = AnswerForm()

    answers = Answer.objects.filter(question=question)
    page_obj = paginate(answers, request)
    return render(request, template_name='question.html',
                  context={"question": question, 'answers': page_obj, 'members': MEMBERS[0:5], 'tags': TAGS[0:5],
                           'page_obj': page_obj, 'form': form})

@csrf_protect
@login_required()
def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            question.save()  # Теперь у вопроса есть ID

            # Обрабатываем и сохраняем теги
            tags_str = form.cleaned_data['tags']
            if tags_str:
                tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                tag_objects = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
                question.tags.set(tag_objects)  # Добавляем Many-to-Many связь

            return redirect('question', question_id=question.pk)
    else:
        form = AskForm()  # Создаем пустую форму для GET-запроса
    return render(request, template_name = 'ask.html', context={'members': MEMBERS[0:5], 'tags': TAGS[0:5], 'form': form})

def layouts(request):
    return render(request, template_name = 'layouts/base.html', context={'members': MEMBERS[0:5], 'tags': TAGS})

@csrf_protect
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                next_url = request.POST.get("continue", "index")
                print(next_url)
                return redirect(next_url)
            form.add_error('username', '') #комментарий к ошибке не выводим
            form.add_error('password', 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, template_name='login.html', context={'members': MEMBERS[0:5], 'tags': TAGS[0:5], 'form': form}) #используем бутстрап 5 с формами

@csrf_protect
@login_required()
def logout(request): #удаляет куки с id сессии
    auth.logout(request)
    referer = request.META.get('HTTP_REFERER', reverse('index')) #вычисляем адрес прошлой страницы, если не задан, то на индекс
    return HttpResponseRedirect(referer)

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)  # Авторизуем пользователя
            return redirect(reverse('index'))
    else:
        form = SignUpForm()

    return render(request, 'signup.html', context={'members': MEMBERS[0:5], 'tags': TAGS[0:5], 'form': form})

@csrf_protect
@login_required #перекидываем в логин не авторизованных пользователей
def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            user = form.save()
            auth.login(request, user)  # Авторизуем пользователя
            return redirect(reverse('settings'))
    else:
        form = SettingsForm(instance=request.user)
    return render(request, template_name = 'settings.html', context={'members': MEMBERS[0:5], 'tags': TAGS[0:5], 'form': form})

def tag(request, tag_name):
    page_obj = paginate(Question.objects.filter_by_tag(tag_name), request)
    return render(request, template_name = 'tag.html', context={'questions': page_obj, "tags": TAGS[0:5], 'members': MEMBERS[0:5], 'tag_name': tag_name, 'page_obj': page_obj})

def hot(request):
    page_obj = paginate(Question.objects.best(), request)
    return render(request, template_name = 'hot.html', context={'hot_questions': page_obj, 'members': MEMBERS[0:5], 'tags': TAGS[0:5], 'page_obj': page_obj})

@csrf_protect
@login_required
def question_like(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)

        existing_like = QuestionLike.objects.filter(question=question, user=request.user.profile).first()

        if existing_like:
            existing_like.delete()
            likes_count = QuestionLike.objects.filter(question=question).count()

            # Обновляем поле likes_count у вопроса
            question.likes_count = likes_count
            question.save()
            return JsonResponse({'count': question.likes_count})

        else:
            QuestionLike.objects.create(question=question, user=request.user.profile)
            likes_count = QuestionLike.objects.filter(question=question).count()

            # Обновляем поле likes_count у вопроса
            question.likes_count = likes_count
            question.save()
            return JsonResponse({'count': question.likes_count})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_protect
@login_required
def answer_like(request, answer_id):
    if request.method == 'POST':
        answer = get_object_or_404(Answer, pk=answer_id)

        existing_like = AnswerLike.objects.filter(answer=answer, user=request.user.profile).first()

        if existing_like:
            existing_like.delete()
            likes_count = AnswerLike.objects.filter(answer=answer).count()

            answer.likes_count = likes_count
            answer.save()
            return JsonResponse({'count': answer.likes_count})

        else:
            AnswerLike.objects.create(answer=answer, user=request.user.profile)
            likes_count = AnswerLike.objects.filter(answer=answer).count()

            answer.likes_count = likes_count
            answer.save()
            return JsonResponse({'count': answer.likes_count})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_protect
@login_required
def mark_correct(request, answer_id):
    if request.method == 'POST':
        answer = get_object_or_404(Answer, pk=answer_id)

        if answer.question.author != request.user.profile:
            return JsonResponse({'error': 'You are not the author of the question'}, status=403)

        answer.is_correct = not answer.is_correct
        answer.save()

        return JsonResponse({'is_correct': answer.is_correct})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
