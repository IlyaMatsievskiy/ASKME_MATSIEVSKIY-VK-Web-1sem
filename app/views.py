from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

TAGS = [{'name': 'Primary'},
        {'name': 'Secondary'},
        {'name': 'Success'},
        {'name': 'Danger'},
        {'name': 'Warning'},
        {'name': 'Info'},
        {'name': 'Light'},
        {'name': 'Dark'}]

QUESTIONS = [
        {
            'id': i,
            'title': f'Question {i}',
            'content': f'long long lore {i}',
            'tags': TAGS[0:4]
        } for i in range(20)
    ]

MEMBERS = [{'name': 'Mr. Stark'},
           {'name': 'Dr. Benner'},
           {'name': 'V. V. Putin'},
           {'name': 'Shaman'},
           {'name': 'E. Mizulina'}]


ANSWERS = [[0] * 10 for k in range(10)]
for i in range(10):
    for j in range(10):
        ANSWERS[i][j] = {
            'id': j,
            'content': f'Long long answer {j}'
        }

def tag_select(questions, tag_name):
    question_list = []
    for i in range(len(questions)):
        tags = questions[i]['tags']
        for j in range(len(tags)):
            if tag_name == tags[j]['name']:
                question_list.append(questions[i])
    return question_list

def paginate(object_list, request, per_page=5):
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
    page_obj = paginate(QUESTIONS, request)
    questions = paginate(QUESTIONS, request)
    return render(request, template_name = 'index.html', context={'questions': questions, 'members': MEMBERS, 'tags': TAGS, 'page_obj': page_obj})

def question(request, question_id):
    ans = ANSWERS[question_id]
    page_obj = paginate(ans, request)
    answers = paginate(ans, request)
    item = QUESTIONS[question_id]
    return render(request, template_name = 'question.html', context={"question": item, 'answers': answers, 'members': MEMBERS, 'tags': TAGS, 'page_obj': page_obj})

def ask(request):
    return render(request, template_name = 'ask.html', context={'members': MEMBERS, 'tags': TAGS})

def layouts(request):
    return render(request, template_name = 'layouts/base.html', context={'members': MEMBERS, 'tags': TAGS})

def login(request):
    return render(request, template_name = 'login.html', context={'members': MEMBERS, 'tags': TAGS})

def signup(request):
    return render(request, template_name = 'signup.html', context={'members': MEMBERS, 'tags': TAGS})

def settings(request):
    return render(request, template_name = 'settings.html', context={'members': MEMBERS, 'tags': TAGS})

def tag(request, tag_name):
    questions = paginate(tag_select(QUESTIONS, tag_name), request)
    page_obj = paginate(tag_select(QUESTIONS, tag_name), request)
    return render(request, template_name = 'tag.html', context={'questions': questions, "tags": TAGS, 'members': MEMBERS, 'tag_name': tag_name, 'page_obj': page_obj})

def hot(request):
    page_obj = paginate(QUESTIONS, request)
    hot_questions = paginate(QUESTIONS, request)
    return render(request, template_name = 'hot.html', context={'hot_questions': hot_questions, 'members': MEMBERS, 'tags': TAGS, 'page_obj': page_obj})
