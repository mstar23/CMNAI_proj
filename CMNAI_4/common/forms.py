from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    family = forms.CharField(label="family")        # 보호자 관계
    phone = forms.Field(label="phone")      # 보호자 번호
    number = forms.Field(label="number")  # 본인 번호


    class Meta:
        model = User
        fields = ("username", "password1", "password2", "family", "phone", "number")