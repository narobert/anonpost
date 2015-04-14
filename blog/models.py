from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

# Create your models here.

class Profile(models.Model):
  user = models.ForeignKey(User)

class Wpost(models.Model):
  id = models.AutoField('#', primary_key=True)
  date = models.DateField(default = datetime.now())
  wallpost = models.CharField(max_length = 1000)
  user = models.ForeignKey(User)

class Ppost(models.Model):
  id = models.AutoField('#', primary_key=True)
  date = models.DateField(default = datetime.now())
  profilepost = models.CharField(max_length = 1000)
  user1 = models.ForeignKey(User, related_name='user1')
  user2 = models.ForeignKey(User, related_name='user2')
  clicked = models.BooleanField(default=False)
