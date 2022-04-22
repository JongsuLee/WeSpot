from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile
from MyOwnColumn.models import Post, Image

# Create your views here.

def sign_up(request):
  context = {}

  if request.method == 'POST':
    if (request.POST.get('id') and
        request.POST.get('password') and
        request.POST.get('password_check') and
        request.POST.get('name') and
        request.POST.get('knickname') and
        request.POST.get('mail')):
        if (request.POST.get('password') == request.POST.get('password_check')):
          new_user = User.objects.create_user(username=request.POST.get('id'),
                                      password=request.POST.get('password'),
                                      last_name=request.POST.get('name'),
                                      first_name=request.POST.get('knickname'),
                                      email=request.POST.get('mail'))
          auth.login(request, new_user)
          profile = Profile(user=new_user, image=request.FILES.get('profile'))
          profile.save()

          return redirect('main')
        else:
          context['password_error'] = '비밀번호가 서로 다릅니다. 다시 확인하여 입력해주세요.'
          
          return redirect('account:sign_up')
    else:
      context['error'] = '모두 입력해주세요.'

      return redirect('account:sign_up')

  return render(request, 'account/sign_up.html', context)

def login(request):
  context = {}

  if request.method == 'POST':
    if request.POST.get('id') and request.POST.get('password'):
      user = auth.authenticate(request, username=request.POST.get('id'), password=request.POST.get('password'))
      if user is not None:
        auth.login(request, user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
      else:
        context['error'] = '아이디와 비밀번호가 일치하지 않습니다.'

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def logout(request):
  if request.method == 'POST':
    auth.logout(request)

  return redirect('main')

def profile(request, username):
  user = User.objects.get(username=username)
  profile = Profile.objects.filter(user=user)
  posts = Post.objects.filter(profile=profile[0])

  context = {
    'profile': profile,
    'posts': posts,
  }

  return render(request, 'account/profile.html', context)