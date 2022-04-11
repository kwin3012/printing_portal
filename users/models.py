from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Order(models.Model):
    # user info
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    # shop keeper info
    shopkeeper_email = models.EmailField(max_length=100)
    shopkeeper_location = models.CharField(max_length=100)

    # file info
    file = models.FileField(blank=False,upload_to='media/')
    no_of_copies = models.IntegerField(default=1)
    black_and_white = models.BooleanField(default=True)

    #order details
    cost = models.IntegerField()
    date_ordered = models.DateTimeField(default=timezone.now)


    









