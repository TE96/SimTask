from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class MyUser(AbstractUser):
    """
    用户信息
    """
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )

    REQUIRED_FIELDS = ('uid', 'email', 'phone')
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    uid = models.IntegerField(primary_key=True)
    phone = models.IntegerField(unique=True)
    email: str = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.username


