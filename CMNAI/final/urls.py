from django.urls import path
from . import views

app_name = 'final'

urlpatterns = [
    path('', views.first_page, name='first_page'),
    path('main_page/', views.main_page, name='main_page'),
    path('diary/', views.diary, name='diary'),
    path('copy/', views.copy, name='copy'),
    path('opencv/', views.opencv, name='opencv'),
    path('hand/', views.hand, name='hand'),
    path('<int:diary_id>/', views.diary_list, name='diary_list'),
    path('diary/create/', views.diary_create, name='diary_create'),
    path('diary/create/<int:diary_id>/', views.diary_create, name='diary_create'),
    path('word_test/', views.word_test, name='word_test'),
    path('word_trans/', views.word_trans, name='word_trans'),
    path('camera_view/', views.camera_view, name='camera_view'),
    path('robot/', views.robot, name="robot"),
    path('mypage_calender/', views.Mood_content, name='mypage_calender'), # 달력 보일 페이지
    path('word/create/theme/', views.word_create, name='theme'),
    path('word/create/f', views.word_create_f, name='word_create_f'),
    path('word/create/a', views.word_create_a, name='word_create_a'),
    path('word/create/p', views.word_create_p, name='word_create_p'),
    path('word/create/v', views.word_create_v, name='word_create_v'),

]