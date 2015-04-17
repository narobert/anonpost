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
  hascomments = models.BooleanField(default = False)
  likes = models.IntegerField(default = 0)
  user = models.ForeignKey(User)

  def for_json(self):
      return {"id": self.id, "likes": self.likes}

class Ppost(models.Model):
  id = models.AutoField('#', primary_key=True)
  date = models.DateField(default = datetime.now())
  profilepost = models.CharField(max_length = 1000)
  user1 = models.ForeignKey(User, related_name='user1')
  user2 = models.ForeignKey(User, related_name='user2')
  hascomments = models.BooleanField(default = False)
  clicked = models.BooleanField(default=False)
  likes = models.IntegerField(default = 0)

  def for_json(self):
      return {"id": self.id, "likes": self.likes}

class Wcomment(models.Model):
  id = models.AutoField('#', primary_key=True)
  date = models.DateField(default = datetime.now())
  wallcomment = models.CharField(max_length = 500)
  wall = models.ForeignKey(Wpost)
  user = models.ForeignKey(User)

  def for_json(self):
      return {"wallcomment": self.wallcomment, "date": self.date.strftime('%B %d, %Y')}

class Pcomment(models.Model):
  id = models.AutoField('#', primary_key=True)
  date = models.DateField(default = datetime.now())
  profilecomment = models.CharField(max_length = 500)
  profile = models.ForeignKey(Ppost)
  user = models.ForeignKey(User)

  def for_json(self):
      return {"profilecomment": self.profilecomment, "date": self.date.strftime('%B %d, %Y')}

class Wlike(models.Model):
  id = models.AutoField('#', primary_key=True)
  wall = models.ForeignKey(Wpost)
  user = models.ForeignKey(User)

class Wdislike(models.Model):
  id = models.AutoField('#', primary_key=True)
  wall = models.ForeignKey(Wpost)
  user = models.ForeignKey(User)

class Plike(models.Model):
  id = models.AutoField('#', primary_key=True)
  profile = models.ForeignKey(Ppost)
  user = models.ForeignKey(User)

class Pdislike(models.Model):
  id = models.AutoField('#', primary_key=True)
  profile = models.ForeignKey(Ppost)
  user = models.ForeignKey(User)
