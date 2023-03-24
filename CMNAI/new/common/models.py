from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator




class User(AbstractUser):
    username = models.CharField(max_length=20, primary_key=True)
    family = models.CharField(max_length=150, blank=True)
    phoneNumberRegex = RegexValidator(regex=r'^01([0]?)-?([0-9]{3,4})-?([0-9]{4})$')
    number = models.CharField(validators=[phoneNumberRegex], max_length=13, unique=True)
    phone = models.CharField(validators=[phoneNumberRegex], max_length=13, unique=True)