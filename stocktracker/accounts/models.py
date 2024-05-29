from django.contrib.auth.models import AbstractUser
from django.db import models

class Account(AbstractUser):
    account_key = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)

