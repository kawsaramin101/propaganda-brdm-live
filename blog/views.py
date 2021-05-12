from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse, reverse_lazy

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .form import CreateBlogPost, CreateBlogComment, CreateBlogCommentReply
from .models import BlogPost, BlogComment, BlogPostCategory
# Create your views here.


 
    

def index(request):
    recentblogpost = BlogPost.objects.filter(is_published=True).order_by('-date_created')
    
    paginator = Paginator(recentblogpost, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
     
    categories = BlogPostCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories
    }
    
    search_input = request.GET.get('search-blog-post')
    if search_input:
        context['page_obj'] = recentblogpost.filter(title__icontains=search_input)
        context['search_input'] = search_input 
        
    return render(request, 'blog/index.html', context)
    
    
    
def category_post(request, category):
    #category = BlogPost.objects.get(id = id)
    category_post_list = BlogPost.objects.filter(category__category=category).order_by('-date_created')
    
    context = {
        'posts': category_post_list,
        'category_name': category
    }
    return render(request, 'blog/category_post.html', context)
    
    
def detail(request, id):
    blogpost = BlogPost.objects.get(id= id)
    total_likes = blogpost.total_likes()
    total_dislikes = blogpost.total_dislikes()
    
    is_liked = False
    is_disliked = False
    if blogpost.likes.filter(id=request.user.id).exists():
        is_liked = True
    if blogpost.dislikes.filter(id=request.user.id).exists():
        is_disliked = True
        
    if request.user != blogpost.author and not blogpost.is_published:
        return HttpResponseNotFound('<h1>Post is not published yet</h1>')
    else:
        context = {
            'blog': blogpost,
            'total_likes': total_likes,
            'total_dislikes': total_dislikes,
            'is_liked': is_liked,
            'is_disliked': is_disliked,
        }
        return render(request, 'blog/detail.html', context)
    
    
    
@login_required(login_url='user:login')
def create_blog_post(request):
    form = CreateBlogPost(request.POST or None)
    author = request.user 
    has_auto = author.has_perm('blog.add_blogpost')
    if request.method == "POST":
        form = CreateBlogPost(request.POST or None)
        if form.is_valid():
            if has_auto:
                form.instance.is_published = True
                messages.info(request, "Blog Post created and published")
            else:
                form.instance.is_published = False
                messages.success(request, 'Blog post created. Wait for an Admin to review your post')
            form.instance.author = author
            form.save()
            
            return redirect(reverse("blog:detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'form': form,
        'has_auto': has_auto
    }
    return render(request, "blog/create_blog.html", context)


@login_required(login_url='user:login')
def update_blog_post(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if request.user != post.author:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        form = CreateBlogPost(request.POST or None, instance=post)
        #author = get_author(request.user)
        #author = request.user
        if request.method == "POST":
            if form.is_valid():
                #form.instance.author = author
                form.save()
                messages.success(request, 'Blog post updated')
            
                return redirect(reverse("blog:detail", kwargs={
                    'id': form.instance.id 
                }))
        context = {
            'form': form
        }
        return render(request, "blog/update_blog.html", context)


@login_required(login_url='user:login')
def delete_post(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if request.user != post.author:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        if request.method == "POST":
            post.delete()
            messages.info(request, 'Blog post deleted')
            
            return redirect(reverse("blog:index"))
        context = {
            'post': post
        }
        return render(request, "blog/delete_blog.html", context)



@login_required(login_url='user:login')
def like_view(request, id):
    post = get_object_or_404(BlogPost, id=id)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        messages.info(request, "Unliked")
    elif post.dislikes.filter(id=request.user.id).exists():
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
        messages.info(request, "Liked")
    else:
        post.likes.add(request.user)
        messages.info(request, "Liked")
        
    return HttpResponseRedirect(reverse('blog:detail', args=[int(id)]))



@login_required(login_url='user:login')
def dislike_view(request, id):
    post = get_object_or_404(BlogPost, id=id)
   
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        messages.info(request, "Disliked Undone")
    elif post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        post.dislikes.add(request.user)
        messages.info(request, "Disliked")
    else:
        post.dislikes.add(request.user)
        messages.info(request, "Disliked")
   
    return HttpResponseRedirect(reverse('blog:detail', args=[int(id)]))




@login_required(login_url='user:login')
def createcomment(request, id):
    commenting_on = get_object_or_404(BlogPost, id=id)
    form = CreateBlogComment()
    
   #author = User.objects.get(username=request.user)
    author = request.user
    if request.method == "POST":
        form = CreateBlogComment(request.POST)
        if form.is_valid():
            print(request.user)
            #comment = form.save(commit=False)
            form.instance.commented_on = commenting_on
            form.instance.author = author
            form.save()
            messages.success(request, 'Comment Added')
            
            return redirect('blog:detail', id=commenting_on.id)
    context = {
        'form': form,
        'post': commenting_on,
    }
    return render(request, "blog/create_comment.html", context)



@login_required(login_url='user:login')
def create_comment_reply(request, id):
    replying_on = get_object_or_404(BlogComment, id=id)
    form = CreateBlogCommentReply(request.POST or None)
    
   #author = User.objects.get(username=request.user)
    author = request.user
    if request.method == "POST":
        form = CreateBlogCommentReply(request.POST or None)
        if form.is_valid():
            print(request.user)
            #comment = form.save(commit=False)
            form.instance.replied_on = replying_on
            form.instance.author = author
            form.save()
            messages.success(request, 'Comment Reply Added')
            
            return redirect('blog:detail', id=replying_on.commented_on.id)
    context = {
        'form': form,
        'replying_on': replying_on,
    }
    return render(request, "blog/create_comment_reply.html", context)

