from django.urls import path
from . import views

app_name = 'myowncolumn'

urlpatterns = [
  path('post/write/', views.write, name='write'),
]