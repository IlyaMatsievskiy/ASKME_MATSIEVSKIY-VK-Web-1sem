from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/edit', views.settings, name='settings'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('hot/', views.hot, name='hot'),
    path('logout/', views.logout, name='logout'), #удаляет куки с id сессии
    path('question/<int:question_id>/like/', views.question_like, name='question_like'),
    path('answer/<int:answer_id>/like/', views.answer_like, name='answer_like'),
    path('answer/<int:answer_id>/mark_correct/', views.mark_correct, name='mark_correct'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)