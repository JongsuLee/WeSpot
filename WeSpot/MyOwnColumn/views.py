from django.shortcuts import render, redirect
from account.models import Profile
from .models import Post, Image, Tag  

# Create your views here.

def write(request):
  profile = Profile.objects.filter(user=request.user)
  context = {
    'profile': profile,
  }

  if request.method == 'POST':
    post = Post(user=request.user, description=request.POST.get('description'))
    post.save()
    
    images = request.FILES.getlist('post_images')
    for image in images:
      img = Image(post=post, image=image)
      img.save()

    if request.POST.get('tag'):
      tags = request.POST.get('tag')
      tags = tags.split('#')[1:]
      for tag in tags:
        tg = Tag(tag=tag)
        tg.save()
        tg.post.add(post)
        tg.save()
        
    
    return redirect('account:profile', request.user.username)

  return render(request, 'myowncolumn/write.html', context)
