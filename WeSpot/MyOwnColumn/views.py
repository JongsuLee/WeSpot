from django.shortcuts import render, redirect
from django.utils import timezone
from account.models import Profile
from .models import Post, Image, Tag  

# Create your views here.

def post_write(request):
  profile = Profile.objects.filter(user=request.user)
  context = {
    'profile': profile,
  }

  if request.method == 'POST':
    profile = Profile.objects.get(user=request.user)
    post = Post(profile=profile, description=request.POST.get('description'), created_at=timezone.now())
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
        
    
    return redirect('myowncolumn:post_detail', post.id)

  return render(request, 'myowncolumn/post_write.html', context)

def post_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  profile = Profile.objects.filter(user=request.user)  

  context = {
    'post': post,
    'profile': profile,
  }

  return render(request, 'myowncolumn/post_detail.html', context)