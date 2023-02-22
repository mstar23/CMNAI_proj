from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    family = models.CharField(max_length=150, blank=True)
    number = models.IntegerField()
    phone = models.IntegerField()