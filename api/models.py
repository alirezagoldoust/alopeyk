from django.db import models
from django.contrib.auth.models import User
import datetime

class ApiKey(models.Model):
    name = models.CharField(max_length=100)
    apikey = models.CharField(max_length=250)
    def __str__(self) -> str:
        return self.name


# This model saves data about users
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20)
    sex = models.CharField(max_length=10, choices=[('m', 'm'), ('f', 'f')], null=True)
    age = models.CharField(max_length=10, null=True)
    def __str__(self) -> str:
        return self.user.username


# This model is for orders
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='customer', null=True)
    # the origin and destination saves lat and long in a string seprated with a comma
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    cost = models.PositiveIntegerField()
    duration = models.DurationField()
    status = models.CharField(max_length=20, choices=[('0','initial'), 
                                                      ('1', 'driver accepted'),
                                                      ('2', 'driver arrived to origin and recieved the box'),
                                                      ('3', 'delivered'),
                                                      ('-1', 'canceled from user'),
                                                      ('-2', 'canceled from driver')], default='0')
    posting_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    has_return = models.BooleanField(default = False)
    driver = models.ForeignKey(User, on_delete=models.PROTECT, null = True, related_name='driver')
    payment = models.CharField(max_length=50, choices=[('0', 'not paid'), ('1', 'online paid')], default='0')

    def __str__(self) -> str:
        return f"{self.customer.username} {self.id}"

    def distance(self, point):
        point = list(map(float, point))
        origin = list(map(float, self.origin.split(',')))
        return (origin[0] - point[0])**2 + (origin[1] - point[1])**2
    


class Feedback(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])