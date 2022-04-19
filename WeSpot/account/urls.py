from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
  path('sign-up/', views.sign_up, name='sign_up'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('profile/<str:username>', views.profile, name='profile'),
]