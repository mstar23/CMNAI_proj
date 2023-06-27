from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import get_user_model
from .models import diary_image


class UserForm(UserCreationForm):
    realname = forms.CharField(label="이름")
    username = forms.CharField(label="별명")
    # password = forms.CharField(label="비밀번호")
    my_phone_number = forms.CharField(label="본인 연락처")
    family = forms.CharField(label="보호자 관계")
    family_phone_number = forms.CharField(label="보호자 연락처")
    

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("realname", "username", "password1", "password2",  "my_phone_number", "family", "family_phone_number")


class MyForm(forms.Form):
    image = forms.ImageField()


class DiaryImageForm(forms.ModelForm):
    class Meta:
        model = diary_image  # 사용할 모델
        fields = ['create_date', 'model_text', 'username', 'realname']
        labels = {
            'create_date': '작성일자',
            'model_text': '일기',
            'username': '별명',
            'realname': '이름'
        }