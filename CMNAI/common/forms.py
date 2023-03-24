from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import get_user_model


class UserForm(UserCreationForm):
    username = forms.CharField(label="아이디")
    # password = forms.CharField(label="비밀번호")
    family = forms.CharField(label="보호자 관계")
    number = forms.CharField(label="보호자 연락처")
    phone = forms.CharField(label="본인 연락처")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2",  "phone", "family", "number")