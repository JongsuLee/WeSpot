from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile

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
        if (request.POST.get('username') and
            request.POST.get('password') == request.POST.get('password_check')):
            new_user = User.objects.create_user(username=request.POST.get('id'),
                                        password=request.POST.get('password'),
                                        last_name=request.POST.get('name'),
                                        first_name=request.POST.get('knickname'),
                                        eamil=request.POST.get('mail'))
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