from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from final import views as final_views


app_name = 'main'

# urlpatterns = [
#     path('login_common/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('signup/', views.signup, name='signup'),
#     path('main_page/', views.main_page, name='main_page'),
#     path('login_main/', views.login_word, name='login_word'),
#     path('abc/', views.upload_image, name='upload')
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    # path('login_common/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # 로그인 / 네비바에서 로그인 눌렀을 때 / login.html로 연결
    path('login_common/', views.login1, name='login'), # 로그인 / 네비바에서 로그인 눌렀을 때 / login.html로 연결
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'), # 로그아웃 / login.html로 연결
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'), # 로그아웃 / login.html로 연결
    path('signup/', views.signup, name='signup'), # 회원가입 / signup.html로 연결
    path('main_page/', views.main_page, name='main_page'), # 메인페이지 / main_page.html로 연결
    path('login_main/', views.login_word, name='login_word'), # 로그인 / 실제로 로그인 할 때 / 손글씨 -> 텍스트 분석과 연결되는 view / 로그인 성공하면 main_page.html, 실패하면 login.html로 연결
    path('upload/', views.upload_image, name='upload'), # 로그인 및 초성퀴즈 분석 결과 POST로 이동하기
    path('upload_diary/', views.upload_image_diary, name='upload_diary'), # 일기 분석 결과 POST로 이동하기
    path('word/create/f', views.word_create_f, name='word_create_f'), # 메인페이지 및 초성퀴즈에서 과일 테마 선택 / word_test_folder/word_test.html로 연결
    path('word/create/a', views.word_create_a, name='word_create_a'), # 메인페이지 및 초성퀴즈에서 동물 테마 선택 / word_test_folder/word_test.html로 연결
    path('word/create/p', views.word_create_p, name='word_create_p'), # 메인페이지 및 초성퀴즈에서 식물 테마 선택 / word_test_folder/word_test.html로 연결
    path('word_test/', views.word_test, name='word_test'), # 초성퀴즈에서 손글씨 -> 텍스트 전환 및 정답 여부 출력 / word_test_folder/word_test.html로 연결
    path('word/create/result/', views.word_result, name='word_result'), # 손글씨 결과창 / word_test_folder/word_score.html로 연결
    path('pose/', views.pose, name='pose'), # 포즈 따라하기 / opencv_folder/pose.html로 연결
    path('camera_view/', views.camera_view, name='camera_view'), # 포즈 기억하기 / opencv_folder/camera_view.html로 연결
    path('robot/', views.robot, name="robot"), # 로보트 / opencv_folder/robot.html로 연결
    path('hand/', views.hand, name='hand'), # 포즈 기억하기 동작
    path('diary/create/', views.diary_create, name='diary_create'), # 일기쓰기 창으로 이동 / diary_folder/diary_form.html로 연결
    path('word_trans/', views.word_trans, name='word_trans'), # 일기 손글씨 텍스트로 전환 / diary_folder/diary_form2.html로 연결
    path('diary/result/', views.diary_result, name='diary_result'), # 텍스트로 전환된 일기창에서 수정을 완료하고 넘어가는 동작
    path('mypage_calender/', views.Mood_content, name='mypage_calender'), # 마이페이지 화면 동작
    path('<int:diary_id>/', views.word_detail, name='word_detail'), # 마이페이지에서 초성퀴즈 내역 눌렀을 때 점수보기 창으로 이동
    path('senti/<int:diary_id>/', views.diary_detail, name='diary_detail'), # 마이페이지에서 일기 날짜 눌렀을 때 보기 창으로 이동

    path('index/', views.index, name='index'), # 초기 페이지 / 로그인 및 메인페이지
    path('index_diary/', views.index_diary, name='index_diary'),
    path('index_diary2/', views.index_diary2, name='index_diary2'),
    path('index_diary_detail/', views.index_diary_detail, name='index_diary_detail'),
    path('index_word/', views.index_word, name='index_word'),
    path('index_signup/', views.index_signup, name='index_signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)