from django.shortcuts import render, redirect
from django.utils import timezone
from account.models import Profile
from .models import Post, Image, PostInColumn, Tag, Column 

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

def column_write(request, column_id):
  profile = Profile.objects.filter(user=request.user)
  column = Column.objects.get(id=column_id)
  posts = Post.objects.filter(columns=column)

  context = {
    'profile': profile,
    'column': column,
    'posts': posts,
  }

  return render(request, 'myowncolumn/column_write.html', context)

def column_add(request, column_id):
  profile = Profile.objects.filter(user=request.user)
  posts =Post.objects.filter(profile=profile[0]).order_by('-id')
  column = Column.objects.get(id=column_id)

  context = {
    'profile': profile,
    'posts': posts,
    'column': column,
  }

  if request.method == 'POST':
    add_ids = request.POST.getlist('add_id')
    for add_id in add_ids:
      post = Post.objects.get(id=add_id)
      post.columns.add(column)
      post.save()

    return redirect('myowncolumn:column_write', column_id=column.id)

  return render(request, 'myowncolumn/column_add.html', context)

def column_detail(request, column_id):
  profile = Profile.objects.filter(user=request.user)
  column = Column.objects.get(id=column_id)
  # posts = PostInColumn.objects.filter(column=column)

  context = {
    'profile': profile,
    'column': column,
  }

  return render(request, 'myowncolumn/column_detail.html', context)