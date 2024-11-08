from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from .models import Answer, Question, Tag, Profile

TAGS = Tag.objects.all()
MEMBERS = Profile.objects.all()

def paginate(object_list, request, per_page=10):
    paginator = Paginator(object_list, per_page)
    page = request.GET.get('page', 1)
    try:
        paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(1)
    else:
        return paginator.page(page)


# Create your views here.
def index(request):
    page_obj = paginate(Question.objects.all(), request)
    return render(request, template_name = 'index.html', context={'questions': page_obj, 'members': MEMBERS[0:5], 'tags': TAGS[0:5], 'page_obj': page_obj})

def question(request, question_id):
    ans = Answer.objects.filter(question=question_id)
    page_obj = paginate(ans, request)
    item = Question.objects.get(id=question_id)
    return render(request, template_name = 'question.html', context={"question": item, 'answers': page_obj, 'members': MEMBERS[0:5], 'tags': TAGS[0:5], 'page_obj': page_obj})

def ask(request):
    return render(request, template_name = 'ask.html', context={'members': MEMBERS[0:5], 'tags': TAGS[0:5]})

def layouts(request):
    return render(request, template_name = 'layouts/base.html', context={'members': MEMBERS[0:5], 'tags': TAGS})

def login(request):
    return render(request, template_name = 'login.html', context={'members': MEMBERS[0:5], 'tags': TAGS[0:5]})

def signup(request):
    return render(request, template_name = 'signup.html', context={'members': MEMBERS[0:5], 'tags': TAGS[0:5]})

def settings(request):
    return render(request, template_name = 'settings.html', context={'members': MEMBERS[0:5], 'tags': TAGS[0:5]})

def tag(request, tag_name):
    page_obj = paginate(Question.objects.filter_by_tag(tag_name), request)
    return render(request, template_name = 'tag.html', context={'questions': page_obj, "tags": TAGS[0:5], 'members': MEMBERS[0:5], 'tag_name': tag_name, 'page_obj': page_obj})

def hot(request):
    page_obj = paginate(Question.objects.best(), request)
    return render(request, template_name = 'hot.html', context={'hot_questions': page_obj, 'members': MEMBERS[0:5], 'tags': TAGS[0:5], 'page_obj': page_obj})
