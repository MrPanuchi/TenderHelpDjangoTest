import datetime

from django.db import models


# Create your models here.

class Nalog(models.Model):
    time = models.DateTimeField(auto_now=True)
    inn = models.CharField(max_length=12, default='000000000000')
    ogrn = models.CharField(max_length=13, default='0000000000000')
    letter = models.CharField(max_length=1000)
