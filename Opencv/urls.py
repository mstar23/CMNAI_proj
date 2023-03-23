from django.urls import path
from . import views

app_name = 'final'

urlpatterns = [
    path('', views.first_page, name='first_page'),
    path('main_page/', views.main_page, name='main_page'),
    path('diary/', views.diary, name='diary'),
    path('copy/', views.copy, name='copy'),
    path('opencv/', views.opencv, name='opencv'),
    path('hand1/', views.hand1, name='hand1'),
    path('hand2/', views.hand2, name='hand2'),
    path('<int:diary_id>/', views.diary_list, name='diary_list'),
    path('diary/create/', views.diary_create, name='diary_create'),
    path('diary/create/<int:diary_id>/', views.diary_create, name='diary_create'),
    path('word_test/', views.word_test, name='word_test'),
    path('word_trans/', views.word_trans, name='word_trans'),
    path('camera_view/', views.camera_view, name='camera_view'),
    path('capture_view/', views.capture_view, name="capture_view"),
    path('opencv_model/', views.opencv_model, name="opencv_model"),
    path('result_sentence/', views.result_sentence, name='result_sentence'),
    path('sentiment/', views.sentiment_page, name='sentiment_page'),
    path('my_page/', views.Mood_content, name='my_page')
]