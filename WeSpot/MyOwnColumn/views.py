from django.shortcuts import render, redirect
from django.utils import timezone
from account.models import Profile
from .models import Post, Image, Tag, Column 

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
  tags = Tag.objects.filter(post=post)  

  context = {
    'post': post,
    'profile': profile,
    'tags': tags,
  }

  return render(request, 'myowncolumn/post_detail.html', context)

def post_edit(request, post_id):
  profile = Profile.objects.filter(user=request.user)
  post = Post.objects.get(id=post_id)
  tags = Tag.objects.filter(post=post)

  context = {
    'profile': profile,
    'post': post,
    'tags': tags
  }

  if request.method == 'POST':
    images = request.FILES.getlist('post_images')
    description = request.POST.get('description')
    tags = request.POST.get('tag')
    if tags:
      tags = tags.split('#')[1:]
    post.description = description
    post.save()
    for image in images:
      img = Image(post=post, image=image)
      img.save()
    for tag in tags:
      tg = Tag(tag=tag)
      tg.save()
      tg.post.add(post)
      tg.save()
    
    return redirect('myowncolumn:post_detail', post_id=post.id)

  return render(request, 'myowncolumn/post_edit.html', context)

def column_create(request):
  profile = Profile.objects.filter(user=request.user)

  context = {
    'profile': profile,
  }

  if request.method == 'POST':
    profile = Profile.objects.get(user=request.user)
    description = request.POST.get('description')
    image = request.FILES.get('image')
    column = Column(profile=profile, description=description, image=image, created_at = timezone.now())
    column.save()
    tags = request.POST.get('tag')
    tags = tags.split('#')[1:]

    for tag in tags:
      tg = Tag(tag=tag)
      tg.save()
      tg.column.add(column)
      tg.save()
    
    return redirect('account:profile', username=profile.user.username)

  return render(request, 'myowncolumn/column_create.html', context)
