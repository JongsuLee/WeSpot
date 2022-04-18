from django.shortcuts import render
from account.models import Profile

def main(request):
  if request.user.is_authenticated:
    profile = Profile.objects.filter(user=request.user)
    context = {
      'profile': profile,
    }
  else:
    context = {}


  return render(request, 'main.html', context)