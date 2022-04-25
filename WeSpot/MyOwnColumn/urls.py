from django.urls import path
from . import views

app_name = 'myowncolumn'

urlpatterns = [
  path('post/write/', views.post_write, name='post_write'),
  path('post/detail/<int:post_id>', views.post_detail, name='post_detail'),
  path('post/edit/<int:post_id>', views.post_edit, name='post_edit'),
  path('column/create/', views.column_create, name='column_create'),
]