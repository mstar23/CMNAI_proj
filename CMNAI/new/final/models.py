from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class diary_image(models.Model):
    username = models.CharField(max_length=20)
    subject = models.DateTimeField()  # 현재 날짜와 시간
    content = models.TextField()  # 이미지 주소
    url_html = models.TextField()  # 이미지 주소
    model_text = models.TextField()  # 모델 분석 텍스트
    # current_content = content.objects.filter(username=current_user)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

class word_image(models.Model):
    username = models.CharField(max_length=20)
    subject = models.DateTimeField()  # 현재 날짜와 시간
    content = models.TextField()  # 이미지 주소
    url_html = models.TextField()  # 이미지 주소
    model_text = models.TextField()  # 모델 분석 텍스트
    create_date = models.DateField()
    modify_date = models.DateTimeField(null=True, blank=True)


class diary_emotion(models.Model):
    username = models.CharField(max_length=20)
    mood = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    date = models.DateField()
    # current_content = content.objects.filter(username=current_user)
    # create_date = models.DateTimeField()
    # modify_date = models.DateTimeField(null=True, blank=True)


    # def __str__(self):
    #     return self.subject


class CameraImage(models.Model):
    image = models.ImageField(upload_to="C://camera//image")
    timestamp = models.DateTimeField(auto_now_add=True)

# class diary_update(models.Model):
#     text = models.ForeignKey(diary_write, on_delete=models.CASCADE)
#     content = diary_write.TextField()
#     create_date = diary_write.DateTimeField()
