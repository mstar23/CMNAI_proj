import json
from django.shortcuts import render, get_object_or_404, redirect  # 파이썬 데이터를 템플릿에 저장하고 html로 띄우기 / 없는 id오면 404 에러
from .models import diary_image, CameraImage, diary_emotion, word_image
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from .forms import DiaryImageForm
from django.core.paginator import Paginator
import cv2
import mediapipe as mp
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from common.models import User
from .aiwrite import last
from .aiwrite2 import last2
from .chosung import chosung_test_f, chosung_test_a, chosung_test_p, chosung_test_v, chosung_reset
from .rnn_model import SequenceClassifier
import os
import random
from kobert_model import predict
from collections import Counter

cho_list = []
tex_list = []
handwrite_list = []
check_list = []
check = ['정답', '오답']

import json
from pymongo import MongoClient

connect = MongoClient("mongodb://localhost:27017")
connect_db = connect['second']  # DB명
connect_col = connect_db['final_diary_emotion'] # 컬렉션명

def Mood_content(request):
    current_user = str(User.objects.get(username=request.user))
    context = list(connect_col.find({"username":current_user}, {"_id": 0}))
    print(context)
    context_json = json.dumps(context, default=str)
    print(context_json)
    return render(request, 'final/mypage_calender.html', {'context_json': context_json}) # 마이페이지 주소



def first_page(request):
    return render(request, 'login.html')

def main_page(request):
    return render(request, 'main_page.html')

def diary(request):
    current_user = User.objects.get(username=request.user)
    current_content = diary_image.objects.filter(username=current_user).order_by('-create_date')
    context = {'diary_list': current_content}

    return render(request, 'final/diary.html', context)

def copy(request):
    return render(request, 'final/copy.html')

def diary_list(request, diary_id):
    diary = get_object_or_404(diary_image, pk=diary_id)
    context = {'diary': diary}
    return render(request, 'final/diary_detail.html', context)

def diary_create(request):
    current_user = User.objects.get(username=request.user)
    current_content = diary_image.objects.filter(username=current_user)
    if request.method == 'POST':  # 질문 등록하면 POST로 방식 변경
        form = DiaryImageForm(request.POST)
        # request.POST에 담긴 subject, content 값이 diaryForm의 subject, content 속성에 자동으로 저장되어 객체가 생성
        if form.is_valid():  # 폼이 유효하다면
            diary = form.save(commit=False)  # 임시 저장하여 diary 객체를 리턴받는다.
            diary.create_date = timezone.now()  # 실제 저장을 위해 작성일시를 설정한다.
            diary.save()  # 데이터를 실제로 저장한다.
            return redirect('final:diary')  # index 함수 호출하기
    else:
        form = DiaryImageForm()
    context = {'form': form}
    return render(request, 'final/diary_form.html', context)

    # 질문 목록 화면에서 "질문 등록하기" 버튼을 클릭한 경우에는 /pybo/diary/create/ 페이지가 GET 방식으로 요청되어 diary_create 함수가 실행된
    # <a href="{% url 'pybo:diary_create' %}" class="btn btn-primary">질문 등록하기</a>와 같이 링크를 통해 페이지를 요청할 경우에는 무조건 GET 방식이 사용되기 때문

def test(request):
    return render(request, 'final/test.html')


def word_test(request):
    return render(request, 'final/word_test.html')

def word_trans(request):
    current_user = User.objects.get(username=request.user)
    word, url, url_html = last.data_storage(current_user)
    word_tok = word.split(".")
    word_tok.pop()
    print("워드 톡은 : ", word_tok)
    result_list = []
    for j in word_tok:
        result = predict(j)
        print("결과는 : ", result)
        result_list += [result]
    print("결과 리스트는 : ", result_list)
    count_items = Counter(result_list)
    max_item = count_items.most_common(n=1)
    print("맥스는 : ", max_item)
    senti = max_item[0][0]
    print(senti)
    mood_color=what_is_your_color(senti)
    print(mood_color)
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
    return render(request, 'final/diary_form.html', context)

def word_create(request):
    return render(request, 'final/theme.html')

def word_create_f(request):
    global cho_list, tex_list, handwrite_list, check_list
    cho_list, tex_list, handwrite_list, check_list = chosung_reset()
    current_user = User.objects.get(username=request.user)
    current_content = word_image.objects.filter(username=current_user)
    # word, url, url_html, cho, tex = last2.data_storage(current_user)
    global cho, tex, theme
    cho, tex, theme = chosung_test_f()
    cho_list.append(cho)
    tex_list.append(tex)
    # form = WordImageForm()
    context = {
        "cho": cho,
        "tex": tex,
        # "result": "맞았습니다!"
    }
    print("word_create")
    print(cho_list)
    print(tex_list)
    print(handwrite_list)
    print(check_list)
    # print(cho)
    # print(tex)
    return render(request, 'final/word_test.html', context)

def word_create_a(request):
    global cho_list, tex_list, handwrite_list, check_list
    cho_list, tex_list, handwrite_list, check_list = chosung_reset()
    current_user = User.objects.get(username=request.user)
    current_content = word_image.objects.filter(username=current_user)
    # word, url, url_html, cho, tex = last2.data_storage(current_user)
    global cho, tex, theme
    cho, tex, theme = chosung_test_a()
    cho_list.append(cho)
    tex_list.append(tex)
    # form = WordImageForm()
    context = {
        "cho": cho,
        "tex": tex,
        # "result": "맞았습니다!"
    }
    print("word_create")
    print(cho_list)
    print(tex_list)
    print(handwrite_list)
    print(check_list)
    # print(cho)
    # print(tex)
    return render(request, 'final/word_test.html', context)

def word_create_p(request):
    global cho_list, tex_list, handwrite_list, check_list
    cho_list, tex_list, handwrite_list, check_list = chosung_reset()
    current_user = User.objects.get(username=request.user)
    current_content = word_image.objects.filter(username=current_user)
    # word, url, url_html, cho, tex = last2.data_storage(current_user)
    global cho, tex, theme
    cho, tex, theme = chosung_test_p()
    cho_list.append(cho)
    tex_list.append(tex)
    # form = WordImageForm()
    context = {
        "cho": cho,
        "tex": tex,
        # "result": "맞았습니다!"
    }
    print("word_create")
    print(cho_list)
    print(tex_list)
    print(handwrite_list)
    print(check_list)
    # print(cho)
    # print(tex)
    return render(request, 'final/word_test.html', context)

def word_create_v(request):
    global cho_list, tex_list, handwrite_list, check_list
    cho_list, tex_list, handwrite_list, check_list = chosung_reset()
    current_user = User.objects.get(username=request.user)
    current_content = word_image.objects.filter(username=current_user)
    # word, url, url_html, cho, tex = last2.data_storage(current_user)
    global cho, tex, theme
    cho, tex, theme = chosung_test_v()
    cho_list.append(cho)
    tex_list.append(tex)
    # form = WordImageForm()
    context = {
        "cho": cho,
        "tex": tex,
        # "result": "맞았습니다!"
    }
    print("word_create")
    print(cho_list)
    print(tex_list)
    print(handwrite_list)
    print(check_list)
    # print(cho)
    # print(tex)
    return render(request, 'final/word_test.html', context)

def word_test(request):
    current_user = User.objects.get(username=request.user)
    word, url, url_html = last2.data_storage(current_user)
    if theme == 'f':
        cho, tex, _ = chosung_test_f()
    if theme == 'a':
        cho, tex, _ = chosung_test_a()
    if theme == 'p':
        cho, tex, _ = chosung_test_p()
    if theme == 'v':
        cho, tex, _ = chosung_test_v()
    cho_list.append(cho)
    tex_list.append(tex)
    handwrite_list.append(word)

    print("word_test")
    print(cho_list)
    print(tex_list)
    print(handwrite_list)
    # if (len(cho_list) - len(handwrite_list)) > 1:
    #     del cho_list[len(handwrite_list):-(len(cho_list)-len(handwrite_list))]
    #     del tex_list[len(handwrite_list):-(len(tex_list)-len(handwrite_list))]
    # print(cho)
    # print(tex)
    # print(word)

    word_image_DB = word_image(username=current_user, subject=timezone.now(), content=url, url_html=url_html , create_date=timezone.now(), model_text=word)
    word_image_DB.save()
    if (word == tex_list[-2]):
        context = {
            "trans": word_image_DB,
            "cho": cho,
            "tex": tex,
            "result": "맞았습니다!"
        }
        check_list.append(check[0])
        print(check_list)
    else:
        context = {
            "trans": word_image_DB,
            "cho": cho,
            "tex": tex,
            "result": "틀렸습니다!"
        }
        check_list.append(check[1])
        print(check_list)
    ratio = (check_list.count('정답') / len(check_list)) * 100
    print(int(ratio))
    return render(request, 'final/word_test.html', context)

def word_trans(request):
    current_user = User.objects.get(username=request.user)
    word, url, url_html = last.data_storage(current_user)
    diary_image_DB = diary_image(username=current_user, subject=timezone.now(), content=url, url_html=url_html , create_date=timezone.now(), model_text=word)
    diary_image_DB.save()
    word_tok = word.split(".")
    # word_tok.pop()
    print("워드 톡은 : ", word_tok)
    result_list = []
    for j in word_tok:
        result = predict(j)
        print("결과는 : ", result)
        result_list += [result]
    print("결과 리스트는 : ", result_list)
    count_items = Counter(result_list)
    max_item = count_items.most_common(n=1)
    print("맥스는 : ", max_item)
    senti = max_item[0][0]
    print(senti)
    mood_color = what_is_your_color(senti)
    print(mood_color)
    diary_emotion_DB = diary_emotion(username=current_user, mood=senti, color=mood_color,
                                     date=timezone.now(), )
    diary_emotion_DB.save()

    context = {
        "trans": diary_image_DB,
        "senti": senti,
        "emotion": diary_emotion_DB
    }
    return render(request, 'final/diary_form.html', context)

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
                    elif (thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0)|(thumb_finger_state == 0 and index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 0 and pinky_finger_state == 0):
                        text = "가위"
                    elif thumb_finger_state == 0 and index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
                        text = "주먹"
                    elif index_finger_state == 1 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 1:
                        text = "Peace"
                    elif thumb_finger_state == 1 and index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 1:
                        text = "Phone"
                    elif index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 0:
                        text = "닭발"
                    elif index_finger_state == 0 and middle_finger_state == 1 and ring_finger_state == 0 and pinky_finger_state == 0:
                        text = "fuck"
                    elif index_finger_state == 0 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 1:
                        text = "ok"
                    elif index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 0 and pinky_finger_state == 0:
                        text = "yeah"
                    elif thumb_finger_state == 1 and index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
                        text = "good"

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
                return redirect('final:opencv')

        return render(request, 'final/opencv.html')


def camera_view(request):
    folder_path = 'C:/Users/mjy30/CMNAI/new/static/'
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
