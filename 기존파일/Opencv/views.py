from django.shortcuts import render, get_object_or_404, redirect  # 파이썬 데이터를 템플릿에 저장하고 html로 띄우기 / 없는 id오면 404 에러
from .models import diary_image, CameraImage
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
from .rnn_model import SequenceClassifier
import os
import random
from.forms import SentenceForm
from kobert_model import predict
import json
from pymongo import MongoClient

connect = MongoClient("mongodb://localhost:27017")
connect_db = connect['secondc']
connect_col = connect_db['final_mood']


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
    #
    diary_image_DB = diary_image(username=current_user, subject=timezone.now(), content=url, url_html=url_html , create_date=timezone.now(), model_text=word)
    diary_image_DB.save()
    return render(request, 'final/diary_form.html')

def opencv(request):
    return render(request, 'final/opencv.html')

def hand1(request):
    max_num_hands = 2 #두개의 손 인식
    gesture = {
        0:'fist', 1:'one', 2:'two', 3:'three', 4:'four', 5:'five',
        6:'six', 7:'rock', 8:'spiderman', 9:'yeah', 10:'ok', 11:'fy'
    } #제스처는
    rps_gesture = {0:'rock', 5:'paper', 9:'scissors', 11:'fuck'}

    # MediaPipe hands model
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        max_num_hands=max_num_hands,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    # Gesture recognition model
    file = np.genfromtxt('C:/37version/new/final/opencv/data/gesture_train_fy.csv', delimiter=',')
    angle = file[:,:-1].astype(np.float32)
    label = file[:, -1].astype(np.float32)
    knn = cv2.ml.KNearest_create()
    knn.train(angle, cv2.ml.ROW_SAMPLE, label)

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            continue

        img = cv2.flip(img, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result = hands.process(img)

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if result.multi_hand_landmarks is not None:
            rps_result = [] #가위,바위,보 결과랑 손의 좌표 저장

            for res in result.multi_hand_landmarks:
                joint = np.zeros((21, 3))
                for j, lm in enumerate(res.landmark):
                    joint[j] = [lm.x, lm.y, lm.z]

                # Compute angles between joints
                v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:] # Parent joint(어른 손)
                v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:] # Child joint(아이 손)
                v = v2 - v1 # [20,3]
                # Normalize v
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                # Get angle using arcos of dot product
                angle = np.arccos(np.einsum('nt,nt->n',
                    v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:],
                    v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

                angle = np.degrees(angle) # Convert radian to degree

                # Inference gesture
                data = np.array([angle], dtype=np.float32)
                ret, results, neighbours, dist = knn.findNearest(data, 3)
                idx = int(results[0][0])

                # Draw gesture result
                if idx in rps_gesture.keys():
                    org = (int(res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0]))
                    cv2.putText(img, text=rps_gesture[idx].upper(), org=(org[0], org[1] + 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

                    rps_result.append({
                        'rps': rps_gesture[idx],#제스처 결과 저장
                        'org': org # 두 개의 손 위치 저장
                    })

                mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

                # Who wins?
                if len(rps_result) >= 2: #손이 두개이상이면
                    winner = None
                    text = ''

                    if rps_result[0]['rps']=='rock': #첫번째 사람(0)이 바위를 내면
                        if rps_result[1]['rps']=='rock'     : text = 'Tie'
                        elif rps_result[1]['rps']=='paper'  : text = 'Paper wins'  ; winner = 1
                        elif rps_result[1]['rps']=='scissors': text = 'Rock wins'   ; winner = 0
                    elif rps_result[0]['rps']=='paper':
                        if rps_result[1]['rps']=='rock'     : text = 'Paper wins'  ; winner = 0
                        elif rps_result[1]['rps']=='paper'  : text = 'Tie'
                        elif rps_result[1]['rps']=='scissors': text = 'Scissors wins'; winner = 1
                    elif rps_result[0]['rps']=='scissors':
                        if rps_result[1]['rps']=='rock'     : text = 'Rock wins'   ; winner = 1
                        elif rps_result[1]['rps']=='paper'  : text = 'Scissors wins'; winner = 0
                        elif rps_result[1]['rps']=='scissors': text = 'Tie'

                    if winner is not None:
                        cv2.putText(img, text='Winner', org=(rps_result[winner]['org'][0], rps_result[winner]['org'][1] + 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 255, 0), thickness=3)
                    cv2.putText(img, text=text, org=(int(img.shape[1] / 2), 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=3)

            cv2.imshow('Game', img)

            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break
                cap.release()
                return redirect('final:opencv')


    return render(request, 'final/opencv.html')

def hand2(request):
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
    folder_path = 'C://37version//new//static//'
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):  # 확장자가 .png인 파일만 리스트에 추가합니다, .jpg 확장자도 원하면 or filename.endswith('.jpg') 추가
            image_paths.append(filename)
    random_image_path = random.choice(image_paths)
    print(random_image_path)
    img_path = {'img_path': random_image_path}
    return render(request, 'final/camera_view.html', img_path)

def capture_view(request): #s:save, q:나가기
    # if not os.path.exists('static'):
    #     os.makedirs('static')
    #
    # cap = cv2.VideoCapture(0)
    #
    #
    # width = int(cap.get(3))  # 가로 길이 가져오기
    # height = int(cap.get(4))  # 세로 길이 가져오기
    # fps = 30
    # cnt = 1
    #
    # fcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    # out = cv2.VideoWriter('static/webcam.avi', fcc, fps, (width, height))
    #
    # while (True):
    #     k = cv2.waitKey(1) & 0xFF
    #     ret, frame = cap.read()
    #     if ret:
    #         out.write(frame)
    #         cv2.imshow('frame', frame)
    #
    #         if k == ord('s'):
    #             print("Screenshot saved...")
    #             cv2.imwrite('static/screenshot{}.jpg'.format(cnt), frame, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])
    #             cnt += 1
    #         elif k == ord('q'):
    #             break
    #     else:
    #         print("Fail to read frame!")
    #         break
    #
    # cap.release()
    # out.release()
    # cv2.destroyAllWindows()
    return render(request, 'final/capture_view.html')

def opencv_model(request):
    import numpy as np
    from PIL import Image

    def mse(image1, image2):
        """
        Calculates the mean squared error between two images.
        """
        # Convert the images to numpy arrays
        im1 = np.array(image1)
        im2 = np.array(image2)

        # Calculate the mean squared error
        mse = np.mean((im1 - im2) ** 2)

        return mse

    # Load the images
    im1 = Image.open("C://37version//new//static//screenshot1.jpg")
    im2 = Image.open("C://37version//new//static//screenshot2.jpg")

    # Calculate the mean squared error
    similarity = mse(im1, im2)

    # Print the similarity
    print("두 이미지 간의 유사성 결과 입니다.:", similarity)

    return redirect('final:opencv')


def sentiment_page(request):
    form = SentenceForm()
    return render(request, 'final/test.html', {'form': form})


def result_sentence(request):
    if request.method == 'POST':
        sentences = request.POST["sentence"]
        result = predict(sentences)
        print("입력: " + sentences)
        print("출력: " + result)
        context = {'sentences': sentences, 'sentences_out': result}
    return render(request, 'final/result.html', context)

def Mood_content(request):
    context = list(connect_col.find({}, {"_id": 0}))
    print(context)
    context_json = json.dumps(context, default=str)
    print(context_json)
    return render(request, 'final/my_page.html', {'context_json': context_json})