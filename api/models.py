from django.db import models
from django.contrib.auth.models import User

class ApiKey(models.Model):
    name = models.CharField(max_length=100)
    apikey = models.CharField(max_length=250)
    def __str__(self) -> str:
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20)
    sex = models.CharField(max_length=10, choices=[('m', 'm'), ('f', 'f')], null=True)
    age = models.CharField(max_length=10, null=True)
    def __str__(self) -> str:
        return self.user.username
