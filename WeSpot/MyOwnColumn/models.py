from django.db import models
from django.contrib.auth.models import User
from account.models import Profile

# Create your models here.

def image_upload_path(instance, filename):

  return '{}/{}'.format(instance.post.profile.user.username, filename)

def column_image_upload_path(instance, filename):

  return 'column/{}/{}'.format(instance.column.profile.user.username, filename)

class Column(models.Model):

  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  description = models.CharField(max_length=200, blank=True)
  image = models.ImageField(upload_to=column_image_upload_path)
  created_at = models.TimeField()

class Post(models.Model):

  profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
  description = models.CharField(max_length=200, blank=True)
  created_at = models.TimeField(null=True)
  columns = models.ManyToManyField(Column, related_name='posts')

class Image(models.Model):

  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  image = models.ImageField(upload_to=image_upload_path)

class Tag(models.Model):

  column = models.ManyToManyField(Column, related_name='tags')
  post = models.ManyToManyField(Post, related_name='tags')
  tag = models.CharField(max_length=100)