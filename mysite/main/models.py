from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


# 사용자 모델
class User(AbstractUser):
    realname = models.CharField(max_length=20)   # 이름
    username = models.CharField(max_length=20, primary_key=True)  # 별명
    family = models.CharField(max_length=150)
    phoneNumberRegex = RegexValidator(regex=r'^01([0]?)-?([0-9]{3,4})-?([0-9]{4})$')
    my_phone_number = models.CharField(validators=[phoneNumberRegex], max_length=13)
    family_phone_number = models.CharField(validators=[phoneNumberRegex], max_length=13)

# 손글씨 이미지 저장 모델
class MyModel(models.Model):
    absolute_image_path = models.ImageField(upload_to='images/')


# 초성퀴즈 데이터
class word_image(models.Model):
    username = models.CharField(max_length=20)  # 별명
    realname = models.CharField(max_length=20)  # 이름
    image_absolute_path = models.TextField()  # 이미지 주소
    image_html_path = models.TextField()  # html에 뿌려줄 이미지 주소
    cho_text = models.TextField()   # 초성 텍스트
    tex_text = models.TextField()   # 정답 텍스트
    model_text = models.TextField()  # 모델 분석 텍스트
    check_text = models.TextField()  # 정답 텍스트
    ratio = models.TextField()  # 정답률
    category = models.TextField() # 테마
    create_date = models.DateTimeField()


# 일기쓰기 데이터
class diary_image(models.Model):
    username = models.CharField(max_length=20)  # 별명
    realname = models.CharField(max_length=20)  # 이름
    image_absolute_path = models.TextField()  # 이미지 주소
    image_html_path = models.TextField()  # 이미지 주소
    model_text = models.TextField()  # 모델 분석 텍스트
    # current_content = content.objects.filter(username=current_user)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    
# 일기 감정 데이터
class diary_emotion(models.Model):
    username = models.CharField(max_length=20)  # 별명
    realname = models.CharField(max_length=20)  # 이름
    mood = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    date = models.DateField()
    # current_content = content.objects.filter(username=current_user)
    # create_date = models.DateTimeField()
    # modify_date = models.DateTimeField(null=True, blank=True)