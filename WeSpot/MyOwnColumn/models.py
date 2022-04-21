from django.db import models
from django.contrib.auth.models import User

from account.models import Profile

# Create your models here.

def image_upload_path(instance, filename):

  return '{}/{}'.format(instance.post.user.username, filename)

class Post(models.Model):

  profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
  description = models.CharField(max_length=200, blank=True)
  created_at = models.TimeField(null=True)

class Image(models.Model):

  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  image = models.ImageField(upload_to=image_upload_path)

class Tag(models.Model):

  post = models.ManyToManyField(Post, related_name='tags')
  tag = models.CharField(max_length=100)