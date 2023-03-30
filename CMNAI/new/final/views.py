import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import diary_image, diary_emotion, word_image
from django.utils import timezone
from .forms import DiaryImageForm
import cv2
import mediapipe as mp
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from common.models import User
from .aiwrite import last
from .aiwrite2 import last2
from .aiwrite3 import last3
from .delete import delete_folder
from .chosung import chosung_test_f, chosung_test_a, chosung_test_p, chosung_reset
import os
import random
from kobert_model import predict
from collections import Counter
from django.core.paginator import Paginator

cho_list = []
tex_list = []
handwrite_list = []
check_list = []
url_list = []
url_html_list = []
check = ['정답', '오답']

from pymongo import MongoClient

connect = MongoClient("mongodb://localhost:27017")
connect_db = connect['second']  # DB명
connect_col = connect_db['final_diary_emotion'] # 감정분석 컬렉션명
connect_col_word = connect_db['final_word_image'] # 단어쓰기 컬렉션명
connect_col_diary = connect_db['final_diary_image'] # 단어쓰기 컬렉션명

def first_page(request):
    return render(request, 'first_page.html')

def main_page(request):
    delete_folder()
    return render(request, 'main_page.html')

def login_word(request):
    word = last3.data_storage() #last3 == airwrite3
    context = {
        "word": word
    }
    return render(request, 'login.html', context)

def copy(request):
    return render(request, 'final/copy.html')

def diary_create(request):
    current_user = User.objects.get(username=request.user)
    form = DiaryImageForm()
    context = {'form': form}
    return render(request, 'final/diary_form.html', context)

def word_test(request):
    return render(request, 'final/word_test.html')

def word_create(request):
    return render(request, 'final/theme.html')

def word_trans(request):
    current_user = User.objects.get(username=request.user)
    word, url, url_html = last.data_storage(current_user)
    word_tok = word.split(".")
    word_tok.pop()
    result_list = []
    for j in word_tok:
        result = predict(j)
        result_list += [result]
    count_items = Counter(result_list)
    max_item = count_items.most_common(n=1)
    senti = max_item[0][0]
    mood_color=what_is_your_color(senti)
    diary_image_DB = diary_image(username=current_user, subject=timezone.now(), content=url, url_html=url_html,
                                 create_date=timezone.now(), model_text=word, )
    diary_image_DB.save()

    diary_emotion_DB = diary_emotion(username=current_user, mood=senti, color=mood_color,
                                   date=timezone.now(),)
    diary_emotion_DB.save()

    context = {
        "trans": diary_image_DB,
        "senti": senti,
        "emotion": diary_emotion_DB
    }
    return render(request, 'final/diary_form2.html', context)

def word_create_f(request):
    global cho_list, tex_list, handwrite_list, check_list
    cho_list, tex_list, handwrite_list, check_list = chosung_reset()
    current_user = User.objects.get(username=request.user)
    global cho, tex, theme
    cho, tex, theme = chosung_test_f()
    cho_list.append(cho)
    tex_list.append(tex)
    if theme == 'f':
        theme = "과일 "
    context = {
        "cho": cho,
        "tex": tex,
        "theme": theme,
    }
    return render(request, 'final/word_test.html', context)

def word_create_a(request):
    global cho_list, tex_list, handwrite_list, check_list
    cho_list, tex_list, handwrite_list, check_list = chosung_reset()
    current_user = User.objects.get(username=request.user)
    global cho, tex, theme
    cho, tex, theme = chosung_test_a()
    cho_list.append(cho)
    tex_list.append(tex)
    if theme == 'a':
        theme = "동물 "
    context = {
        "cho": cho,
        "tex": tex,
        "theme": theme,
    }
    return render(request, 'final/word_test.html', context)

def word_create_p(request):
    global cho_list, tex_list, handwrite_list, check_list
    cho_list, tex_list, handwrite_list, check_list = chosung_reset()
    current_user = User.objects.get(username=request.user)
    global cho, tex, theme
    cho, tex, theme = chosung_test_p()
    cho_list.append(cho)
    tex_list.append(tex)
    if theme == 'p':
        theme = "식물 "
    context = {
        "cho": cho,
        "tex": tex,
        "theme": theme,
    }
    return render(request, 'final/word_test.html', context)

def word_create_v(request):
    global cho_list, tex_list, handwrite_list, check_list
    cho_list, tex_list, handwrite_list, check_list = chosung_reset()
    current_user = User.objects.get(username=request.user)
    global cho, tex, theme
    cho, tex, theme = chosung_test_v()
    cho_list.append(cho)
    tex_list.append(tex)
    context = {
        "cho": cho,
        "tex": tex,
    }
    return render(request, 'final/word_test.html', context)

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
        category = "🥦식물🍁"
    if theme == 'v':
        cho, tex, _ = chosung_test_v()
        category = "🚙교통수단🚎"

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
    return render(request, 'final/word_test.html', context)

def word_result(request):
    current_user = str(User.objects.get(username=request.user))
    ratio = int((check_list.count('정답') / len(check_list)) * 100)
    word_image_DB = word_image(username=current_user, subject=timezone.now(), content=url_list, url_html=url_html_list , create_date=timezone.now(), model_text=handwrite_list, cho_text=cho_list, tex_text=tex_list, check_text=check_list, ratio=ratio, category=category)
    word_image_DB.save()
    context = list(connect_col_word.find({"username": current_user}, {"_id": 0}))[-1]
    context_json_word = json.dumps(context, default=str)
    print(context_json_word)
    delete_folder()
    return render(request, 'final/diary_detail.html', {'context_json_word': context_json_word})

def diary(request): # mypage 게시판 목록
    current_user = User.objects.get(username=request.user)
    current_content = word_image.objects.filter(username=current_user).order_by('-create_date')
    context = {'context_json_word': current_content}
    return render(request, 'final/diary.html', context)

def diary_list(request, diary_id): # mypage게시판에서 글을 눌렀을 때
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
    delete_folder()
    return render(request, 'final/diary_detail.html', context)

def diary_list2(request, diary_id): # 눌렀을 때 나오는일기장
    diary = get_object_or_404(diary_image, pk=diary_id)
    context = {'diary': diary}
    delete_folder()
    return render(request, 'final/diary_detail2.html', context)


def diary_result(request): # 일기쓰고 내 손글씨 나오는 부분
    current_user = str(User.objects.get(username=request.user))
    context_json_word = list(connect_col_diary.find({"username": current_user}, {"_id": 0}))[-1]
    context = {'diary': context_json_word}
    delete_folder()
    return render(request, 'final/diary_detail2.html', context)

def Mood_content(request):
    page = request.GET.get('page', '1')  # 페이지
    current_user = str(User.objects.get(username=request.user))
    context = list(connect_col.find({"username":current_user}, {"_id": 0}))                 # 감정분석
    current_content = word_image.objects.filter(username=current_user).order_by('-subject')     # 게시판에 초성퀴즈 목록
    paginator = Paginator(current_content, 5)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context_json = json.dumps(context, default=str)     # 감정분석
    return render(request, 'final/mypage_calender.html',{'context_json': context_json, 'diary_list': page_obj})  # 마이페이지 주소

# 기분을 색으로 변환
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

def opencv(request):
    return render(request, 'final/opencv.html')


def hand(request):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    mp_drawing_styles = mp.solutions.drawing_styles

    # For webcam input:
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

        while cap.isOpened():
            success, image = cap.read()

            if not success:
                print("Ignoring empty camera frame.")

                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_height, image_width, _ = image.shape

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    # 엄지를 제외한 나머지 4개 손가락의 마디 위치 관계를 확인하여 플래그 변수를 설정합니다. 손가락을 일자로 편 상태인지 확인합니다.
                    thumb_finger_state = 0
                    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * image_height > \
                            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * image_height > \
                                hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * image_height > \
                                    hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height:
                                thumb_finger_state = 1

                    index_finger_state = 0
                    if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * image_height > \
                            hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height > \
                                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height > \
                                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height:
                                index_finger_state = 1

                    middle_finger_state = 0
                    if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * image_height > \
                            hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height > \
                                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height > \
                                    hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height:
                                middle_finger_state = 1

                    ring_finger_state = 0
                    if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * image_height > \
                            hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height > \
                                hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height > \
                                    hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height:
                                ring_finger_state = 1

                    pinky_finger_state = 0
                    if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y * image_height > \
                            hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * image_height > \
                                hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * image_height > \
                                    hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height:
                                pinky_finger_state = 1

                    # 손가락 위치 확인한 값을 사용하여 가위,바위,보 중 하나를 출력 해줍니다.
                    font = ImageFont.truetype("fonts/gulim.ttc", 80)
                    image = Image.fromarray(image)
                    draw = ImageDraw.Draw(image)

                    text = ""
                    if thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 1:
                        text = "보"
                    elif ((thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0)|(thumb_finger_state == 0 and index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 0 and pinky_finger_state == 0)):
                        text = "가위"
                    elif thumb_finger_state == 0 and index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
                        text = "주먹"
                    elif index_finger_state == 1 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 1:
                        text = "여우"
                    elif thumb_finger_state == 1 and index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 1:
                        text = "전화"
                    elif index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 0:
                        text = "닭발"
                    elif index_finger_state == 0 and middle_finger_state == 1 and ring_finger_state == 0 and pinky_finger_state == 0:
                        text = "산"
                    elif index_finger_state == 0 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 1:
                        text = "오케이"
                    elif index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 0 and pinky_finger_state == 0:
                        text = "김치~"
                    elif thumb_finger_state == 1 and index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
                        text = "최고"

                    w, h = font.getsize(text)

                    x = 50
                    y = 50

                    draw.rectangle((x, y, x + w, y + h), fill='black')
                    draw.text((x, y), text, font=font, fill=(255, 255, 255))
                    image = np.array(image)

                    # 손가락 뼈대를 그려줍니다.
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            cv2.imshow('MediaPipe Hands', image)

            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break
                cap.release()

        return render(request, 'main_page.html')


def camera_view(request):
    folder_path = 'C://Users//mjy30//CMNAI//new//static'
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):  # 확장자가 .png인 파일만 리스트에 추가합니다, .jpg 확장자도 원하면 or filename.endswith('.jpg') 추가
            image_paths.append(filename)
    random_image_path = random.choice(image_paths)
    print(random_image_path)
    img_path = {'img_path': random_image_path}
    return render(request, 'final/camera_view.html', img_path)

def robot(request):
    return render(request, 'final/robot.html')

def pose(request):
    return render(request, 'final/pose.html')

