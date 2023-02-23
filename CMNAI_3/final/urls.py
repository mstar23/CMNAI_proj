from django.urls import path
from . import views

app_name = 'final'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),   # config/urls.py 수정 필요 : path('final/',  include('final.urls')),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
]