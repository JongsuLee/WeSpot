from email.mime import image
from django.contrib import admin
from .models import Post, Image,Column

# Register your models here.

admin.site.register(Column)
admin.site.register(Post)
admin.site.register(Image)