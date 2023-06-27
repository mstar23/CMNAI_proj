import json
import cv2
import os
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from main.models import User
from django.contrib.auth import authenticate, login     # 사용자 인증 / 로그인
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, DiaryImageForm
from django.contrib.auth import get_user_model
from .chosung import chosung_test_f, chosung_test_a, chosung_test_p, chosung_reset
from .aiwrite import last
from .aiwrite2 import last2
from .aiwrite3 import last3
from .aiwrite4 import last4
from .models import MyModel, word_image, diary_image, diary_emotion
import base64
from django.conf import settings
from pymongo import MongoClient
from django.utils import timezone
import random
import mediapipe as mp
from collections import Counter
from kobert_model import predict
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.template.defaultfilters import safe
from datetime import datetime
import pytz


User = get_user_model()

cho_list = []
tex_list = []
handwrite_list = []
check_list = []
url_list = []
url_html_list = []
check = ['정답', '오답']
word = ""

connect = MongoClient("mongodb://localhost:27017")
connect_db = connect['main_db']  # DB명
connect_col = connect_db['main_diary_emotion'] # 감정분석 컬렉션명
connect_col_user = connect_db['main_user'] # 회원 컬렉션명
connect_col_word = connect_db['main_word_image'] # 단어쓰기 컬렉션명
connect_col_diary = connect_db['main_diary_image'] # 일기쓰기 컬렉션명


# 테스트용
def index(request):
    return render(request, 'index.html')

def index_diary(request):
    return render(request, 'index_diary.html')

def index_diary2(request):
    return render(request, 'index_diary2.html')

def index_diary_detail(request):
    return render(request, 'index_diary_detail.html')

def index_word(request):
    return render(request, 'index_word.html')

def index_signup(request):
    return render(request, 'index_signup.html')

# 로그인
def login1(request):
    if request.method == "POST":
        if len(list(connect_col_user.find({"username": nick}))) == 0 :
            print("별명 안맞음")
            return render(request, 'index_errors.html')
        if len(list(connect_col_user.find({"realname": name}))) == 0 :
            print("실제 이름 안맞음")
            return render(request, 'index_errors.html')
        context = list(connect_col_user.find({"username": nick}, {"_id": 0}))[-1]
        # print(context["nickname"])
        if context["realname"] == name:
            username = nick
            raw_password = "qwer1234!"
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            # return redirect('main:main_page')
            return redirect('main:index')
    else: # Get 요청
        form = UserForm()
    # return render(request, 'login.html', {'form': form})
    return render(request, 'index.html')

connect_col_user_all = []  # 초기화

# 회원가입
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            print("폼 미쳤다!!!!")
            form.save()
            username = form.cleaned_data.get('username')
            print(username)
            raw_password = form.cleaned_data.get('password1')
            # form.cleaned_data.get : 폼의 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수로 여기서는 인증시 사용할 사용자명과 비밀번호를 얻기 위해 사용
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            # return redirect('main:main_page')
            return redirect('main:index')
        else: # Get 요청
            print("GET!!!!!!!!!!!!!!!!!!!!")
            form = UserForm()
            connect_col_nick_all = list(connect_col_user.distinct("username"))
            connect_col_nick_all_json = json.dumps(connect_col_nick_all)
    return render(request, 'signup.html', {'form': form, 'connect_col_nick_all': connect_col_nick_all_json})
    # return render(request, 'index_signup.html', {'form': form})

# 첫 화면
def first(request):
    return render(request, 'login.html')



# 로그인 할 때 손글씨 -> 텍스트 전환
def login_word(request):
    global name, nick
    print("login")
    word_list = []
    name = last3.data_storage()
    # word_list.append(name)
    nick = last4.data_storage()
    # word_list.append(nick)
    # connect_col_user_all = list(connect_col_user.distinct("username"))
    # print(connect_col_user_all)
    context = {
        "word": name,
        "nick": nick,
        # "allname": connect_col_user_all
    }
    if name == "":
        return render(request, 'index_errors.html')
    if nick == "":
        return render(request, 'index_errors.html')
    return render(request, 'index.html', context)

# 메인페이지
def main_page(request):
    # delete_folder()
    return render(request, 'main_page.html')

# 테스트용
def abc(request):
    # delete_folder()
    return render(request, 'abc.html')


################################

# 로그인 및 초성퀴즈 시 Ajax에 의해 서버에 저장된 이미지(손글씨)를 Django 디렉토리 및 DB에 저장
# def upload_image(request):
#     if request.method == 'POST':
#         image_data = request.POST.get('image_data')
#         if image_data:
#             # 이미지 데이터가 전달된 경우
#             # 이미지 파일로 저장
#             img_data = image_data.split(',')[1]  # 이미지 데이터에서 헤더 제거
#             img_data = base64.b64decode(img_data)
#             file_name = 'image12.jpg'  # 저장할 파일명 설정
#             path_child = "/images/"
#             # file_path = os.path.join(settings.MEDIA_ROOT, path_child)
#             file_path = settings.MEDIA_ROOT + path_child + file_name
#             print(file_path)
#             with open(file_path, 'wb') as f:
#                 f.write(img_data)
#
#             # 모델에 이미지 경로 저장
#             # MyModel.objects.create(image='images/' + file_name)
#             MyModel.objects.create(absolute_image_path=file_path)
#             return render(request, 'main_page.html')
#             # return redirect('main:main_page')
#     else:
#         form = UserForm()
#     return render(request, 'login.html')


# 로그인 및 초성퀴즈 시 Ajax에 의해 서버에 저장된 이미지(손글씨)를 Django 디렉토리 및 DB에 저장
def upload_image(request):
    print("upload_image 1")
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        print("upload_image 2")
        if image_data:
            # 이미지 데이터가 전달된 경우
            # 이미지 파일로 저장
            img_data = image_data.split(',')[1]  # 이미지 데이터에서 헤더 제거
            img_data = base64.b64decode(img_data)

            # jsCanvas 이미지 저장
            js_canvas_file_name = '/image_login_top_and_chosung_quiz.jpg'
            path_child = "/images/"
            # file_path = os.path.join(settings.MEDIA_ROOT, path_child)
            js_canvas_path = settings.MEDIA_ROOT + path_child + js_canvas_file_name
            # js_canvas_path = settings.MEDIA_ROOT + js_canvas_file_name
            with open(js_canvas_path, 'wb') as f:
                f.write(img_data)

            # canvas_top 이미지 저장
            canvas_bot_data = request.POST.get('canvas_bot_data')
            print("upload_image 3")
            if canvas_bot_data:
                canvas_bot_img_data = canvas_bot_data.split(',')[1]  # 이미지 데이터에서 헤더 제거
                canvas_bot_img_data = base64.b64decode(canvas_bot_img_data)
                canvas_bot_file_name = '/image_login_bot.jpg'
                # canvas_top_path = settings.MEDIA_ROOT + canvas_top_file_name
                path_child = "/images/"
                # file_path = os.path.join(settings.MEDIA_ROOT, path_child)
                canvas_bot_path = settings.MEDIA_ROOT + path_child + canvas_bot_file_name
                with open(canvas_bot_path, 'wb') as f:
                    f.write(canvas_bot_img_data)

            # 모델에 이미지 경로 저장
            MyModel.objects.create(absolute_image_path=js_canvas_path)
            if canvas_bot_data:
                MyModel.objects.create(absolute_image_path=canvas_bot_path)

            return render(request, 'main_page.html')
    else:
        form = UserForm()

    return render(request, 'login.html')

# 일기쓰기 시 Ajax에 의해 서버에 저장된 이미지(손글씨)를 Django 디렉토리 및 DB에 저장
def upload_image_diary(request):
    print("upload_image_diary 1")
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        print("upload_image_diary 2")
        if image_data:
            # 이미지 데이터가 전달된 경우
            # 이미지 파일로 저장
            img_data = image_data.split(',')[1]  # 이미지 데이터에서 헤더 제거
            img_data = base64.b64decode(img_data)

            # jsCanvas 이미지 저장
            js_canvas_file_name = '/image_bottom.jpg'
            path_child = "/images/"
            # file_path = os.path.join(settings.MEDIA_ROOT, path_child)
            js_canvas_path = settings.MEDIA_ROOT + path_child + js_canvas_file_name
            # js_canvas_path = settings.MEDIA_ROOT + js_canvas_file_name
            with open(js_canvas_path, 'wb') as f:
                f.write(img_data)

            # canvas_top 이미지 저장
            canvas_top_data = request.POST.get('canvas_top_data')
            print("upload_image_diary 3")
            if canvas_top_data:
                canvas_top_img_data = canvas_top_data.split(',')[1]  # 이미지 데이터에서 헤더 제거
                canvas_top_img_data = base64.b64decode(canvas_top_img_data)
                canvas_top_file_name = '/image_top.jpg'
                # canvas_top_path = settings.MEDIA_ROOT + canvas_top_file_name
                path_child = "/images/"
                # file_path = os.path.join(settings.MEDIA_ROOT, path_child)
                canvas_top_path = settings.MEDIA_ROOT + path_child + canvas_top_file_name
                with open(canvas_top_path, 'wb') as f:
                    f.write(canvas_top_img_data)

            # 모델에 이미지 경로 저장
            MyModel.objects.create(absolute_image_path=js_canvas_path)
            if canvas_top_data:
                MyModel.objects.create(absolute_image_path=canvas_top_path)

            return render(request, 'main_page.html')
    else:
        form = UserForm()

    return render(request, 'login.html')


# 메인페이지에서 과일 초성 테마 눌렀을 때
def word_create_f(request):
    global cho_list, tex_list, handwrite_list, check_list, category
    cho_list, tex_list, handwrite_list, check_list = chosung_reset()
    current_user = User.objects.get(username=request.user)
    print(current_user)
    print("current_usercurrent_usercurrent_usercurrent_usercurrent_user")
    global cho, tex, theme
    cho, tex, theme = chosung_test_f()
    cho_list.append(cho)
    tex_list.append(tex)
    if theme == 'f':
        theme = "과일 "
        category = "🍓과일🍌"
    context = {
        "cho": cho,
        "tex": tex,
        "theme": theme,
    }
    # return render(request, 'word_test_folder/word_test.html', context)
    return render(request, 'index_word.html', context)

# 메인페이지에서 동물 초성 테마 눌렀을 때
def word_create_a(request):
    global cho_list, tex_list, handwrite_list, check_list, category
    cho_list, tex_list, handwrite_list, check_list = chosung_reset()
    current_user = User.objects.get(username=request.user)
    global cho, tex, theme
    cho, tex, theme = chosung_test_a()
    cho_list.append(cho)
    tex_list.append(tex)
    if theme == 'a':
        theme = "동물 "
        category = "😺동물🐘"
    context = {
        "cho": cho,
        "tex": tex,
        "theme": theme,
    }
    # return render(request, 'word_test_folder/word_test.html', context)
    return render(request, 'index_word.html', context)
# 메인페이지에서 식물 초성 테마 눌렀을 때
def word_create_p(request):
    global cho_list, tex_list, handwrite_list, check_list, category
    cho_list, tex_list, handwrite_list, check_list = chosung_reset()
    current_user = User.objects.get(username=request.user)
    global cho, tex, theme
    cho, tex, theme = chosung_test_p()
    cho_list.append(cho)
    tex_list.append(tex)
    if theme == 'p':
        theme = "식물 "
        category = "🌹식물🍁"
    context = {
        "cho": cho,
        "tex": tex,
        "theme": theme,
    }
    # return render(request, 'word_test_folder/word_test.html', context)
    return render(request, 'index_word.html', context)
# 초성퀴즈에서 손글씨 -> 텍스트 전환 및 정답 여부 출력
def word_test(request):
    global url_list, url_html_list, ratio, category, cho, tex
    current_user = User.objects.get(username=request.user)
    word, url, url_html = last2.data_storage(current_user)
    if theme == '과일 ':
        cho, tex, _ = chosung_test_f()
        category = "🍓과일🍌"
    if theme == '동물 ':
        cho, tex, _ = chosung_test_a()
        category = "😺동물🐘"
    if theme == '식물 ':
        cho, tex, _ = chosung_test_p()
        category = "🌹식물🍁"
    # if theme == 'v':
    #     cho, tex, _ = chosung_test_v()
    #     category = "🚙교통수단🚎"

    print(theme)
    cho_list.append(cho)
    tex_list.append(tex)
    handwrite_list.append(word)
    url_list.append(url)
    url_html_list.append(url_html)

    if (word == tex_list[-2]):
        result= "맞았습니다!⭕"
        check_list.append(check[0])
        print(check_list)
    else:
        result= "틀렸습니다!❌"
        check_list.append(check[1])
        print(check_list)
    ratio = (check_list.count('정답') / len(check_list)) * 100
    print(int(ratio))
    context = {
        "cho": cho,
        "tex": tex,
        "result": result,
        "category": category,
        "theme": theme
    }
    # return render(request, 'word_test_folder/word_test.html', context)
    return render(request, 'index_word.html', context)

# 초성퀴즈 결과 보기
def word_result(request):
    current_user = str(User.objects.get(username=request.user))
    realname = connect_col_user.find_one({"username": current_user})['realname']
    if len(check_list) > 0 :
        ratio = int((check_list.count('정답') / len(check_list)) * 100)
    else:
        ratio = 0
    word_image_DB = word_image(username=current_user, realname=realname, image_absolute_path=url_list, image_html_path=url_html_list , cho_text=cho_list, tex_text=tex_list, model_text=handwrite_list, check_text=check_list, ratio=ratio, category=category, create_date=timezone.now())
    word_image_DB.save()
    context = list(connect_col_word.find({"username": current_user}, {"_id": 0}))[-1]
    context_json_word = json.dumps(context, default=str)
    # return render(request, 'word_test_folder/word_score.html', {'context_json_word': context_json_word})
    return render(request, 'index_word_score.html', {'context_json_word': context_json_word})

# 일기쓰기로 이동
def diary_create(request):
    current_user = User.objects.get(username=request.user)
    form = DiaryImageForm()
    context = {'form': form}
    # return render(request, 'diary_folder/diary_form.html', context)
    return render(request, 'index_diary.html', context)

# 일기 손글씨 텍스트로 전환
def word_trans(request):
    current_user = str(User.objects.get(username=request.user))
    word, url, url_html = last.data_storage(current_user)
    realname = connect_col_user.find_one({"username": current_user})['realname']
    word_tok = word.split(".")
    word_tok.pop()
    result_list = []
    for j in word_tok:
        result = predict(j)
        result_list += [result]
    count_items = Counter(result_list)
    max_item = count_items.most_common(n=1)
    if len(max_item) == 0:
        print("max 없음")
        diary_image_DB = diary_image(username=current_user, realname=realname, image_absolute_path=url, image_html_path=url_html,
                                     model_text=word, create_date=timezone.now())
        diary_image_DB.save()

        diary_emotion_DB = diary_emotion(username=current_user, realname=realname, mood="", color="",
                                         date=timezone.now(), )
        diary_emotion_DB.save()

        context = {
            "trans": diary_image_DB,
        }
        return render(request, 'index_diary_errors.html', context)
    senti = max_item[0][0]
    mood_color=what_is_your_color(senti)
    diary_image_DB = diary_image(username=current_user, realname=realname, image_absolute_path=url, image_html_path=url_html,
                                 model_text=word, create_date=timezone.now())
    diary_image_DB.save()

    diary_emotion_DB = diary_emotion(username=current_user, realname=realname, mood=senti, color=mood_color,
                                   date=timezone.now(),)
    diary_emotion_DB.save()

    context = {
        "trans": diary_image_DB,
        "senti": senti,
        "emotion": diary_emotion_DB
    }
    print("max 있음")
    # return render(request, 'diary_folder/diary_form2.html', context)
    return render(request, 'index_diary2.html', context)

# 텍스트로 전환된 일기창에서 수정을 완료하고 넘어가는 동작
def diary_result(request):
    current_user = str(User.objects.get(username=request.user))
    context_json_word = list(connect_col_diary.find({"username": current_user}, {"_id": 0}))[-1]
    utc = pytz.timezone('UTC')
    seoul = pytz.timezone('Asia/Seoul')
    create_date = context_json_word['create_date'].replace(tzinfo=utc).astimezone(seoul)
    context_json_word['create_date'] = create_date
    context = {'diary': context_json_word}
    # return render(request, 'diary_folder/diary_detail.html', context)
    return render(request, 'index_diary_detail.html', context)

# 감정을 색으로 변환
def what_is_your_color(feel):
    yourcolor = "white"
    emotion_color = {"불안": "#7E7474E0", "당황": "#F18746F7", '슬픔': "#6397E7FF", '분노': "#EE6060FF", '상처': "#8BC065FF ", '기쁨': "#F8F05AF7"}
    for e in emotion_color.keys():
        if feel != e:
            continue
        else:
            yourcolor = emotion_color[feel]
            # 변수 할당후 시작 안하면 local variable 'yourcolor' referenced before assignment 오류
            return yourcolor
        
# 마이페이지 화면 전체
def Mood_content(request):
    page = request.GET.get('page', '1')  # 페이지
    current_user = str(User.objects.get(username=request.user))
    context = list(connect_col.find({"username":current_user}, {"_id": 0}))                 # 감정분석
    current_content = word_image.objects.filter(username=current_user).order_by('-create_date')     # 게시판에 초성퀴즈 목록
    paginator = Paginator(current_content, 5)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context_json = json.dumps(context, default=str)     # 감정분석
    # return render(request, 'mypage_folder/mypage_calender.html',{'context_json': context_json, 'obj_list': page_obj})  # 마이페이지 주소
    return render(request, 'index_mypage_calender.html',{'context_json': context_json, 'obj_list': page_obj})  # 마이페이지 주소

# 마이페이지에서 초성퀴즈 눌렀을 때 점수 나오기 동작
def word_detail(request, diary_id):
    current_user = str(User.objects.get(username=request.user))
    context_json_word = list(connect_col_word.find({"username": current_user}, {"_id": 0}))
    for data in context_json_word:
        if data['id'] == diary_id:
            context_json_word = json.dumps(data, default=str)
            print(data)
    diary = get_object_or_404(word_image, pk=diary_id)
    context = {'context_json_word': context_json_word, "diary":diary}
    print("다이어리 리스트")
    print(context)
    # return render(request, 'word_test_folder/word_score.html', context)
    return render(request, 'index_word_score.html', context)

# 마이페이지에서 일기 눌렀을 때 일기이미지 나오기 동작
def diary_detail(request, diary_id):
    diary = get_object_or_404(diary_image, pk=diary_id)
    context = {'diary': diary}
    # return render(request, 'diary_folder/diary_detail.html', context)
    return render(request, 'index_diary_detail.html', context)

# 포즈 따라하기
def pose(request):
    return render(request, 'opencv_folder/pose.html')

# 포즈 맞추기
def camera_view(request):
    folder_path = '/mnt/c/Users/ska06/PycharmProjects/pythonProject1/mysite/media/opencv_images'
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):  # 확장자가 .png인 파일만 리스트에 추가합니다, .jpg 확장자도 원하면 or filename.endswith('.jpg') 추가
            image_paths.append(filename)
    random_image_path = random.choice(image_paths)
    img_path = {'img_path': random_image_path}
    # return render(request, 'opencv_folder/camera_view.html', img_path)
    return render(request, 'index_camera_view.html', img_path)

# 로보트
def robot(request):
    # return render(request, 'opencv_folder/robot.html')
    return render(request, 'index_robot.html')


