from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    family = forms.CharField(label="가족관계")
    f_HP = forms.Field(label="자녀연락처")
    address = forms.CharField(label="주소")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "family", "f_HP", "address")