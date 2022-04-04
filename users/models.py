from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser
from django.forms import CharField, EmailField, FileField
from django.utils import timezone


# Create your models here.

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)

class Order(models.Model):
    # user info
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    # shop keeper info
    shopkeeper_email = models.EmailField(max_length=100)
    shopkeeper_location = models.CharField(max_length=100)

    # file info
    file = models.FileField(default="blank.pdf",upload_to='')
    no_of_copies = models.IntegerField(default=1)
    black_and_white = models.BooleanField(default=True)

    #order details
    cost = models.IntegerField()
    date_ordered = models.DateTimeField(default=timezone.now)









