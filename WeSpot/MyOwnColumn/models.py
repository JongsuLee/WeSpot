from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def image_upload_path(instance, filename):

  return '{}/{}'.format(instance.post.user.username, filename)

class Post(models.Model):

  user = models.ForeignKey(User, on_delete=models.PROTECT)
  description = models.CharField(max_length=200, blank=True)

class Image(models.Model):

  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  image = models.ImageField(upload_to=image_upload_path)

class Tag(models.Model):

  post = models.ManyToManyField(Post, related_name='tags')
  tag = models.CharField(max_length=100)