from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Tag, Like, Comment, Follow, Bookmark, UserProfile
from .forms import PostForm, CommentForm, UserProfileForm

def home(request):
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'blog/home.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status='published')
    
    # Increment view count
    post.views_count += 1
    post.save()
    
    # Check if user liked the post
    user_liked = False
    user_bookmarked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, post=post).exists()
        user_bookmarked = Bookmark.objects.filter(user=request.user, post=post).exists()
    
    # Get comments
    comments = Comment.objects.filter(post=post, parent=None).select_related('author')
    
    # Handle comment form
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            # Update comment count
            post.comments_count = post.comments.count()
            post.save()
            
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'user_liked': user_liked,
        'user_bookmarked': user_bookmarked,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

# @login_required
# def like_post(request, pk):
#     if request.method == 'POST':
#         post = get_object_or_404(Post, pk=pk)
#         like, created = Like.objects.get_or_create(user=request.user, post=post)
        
#         if not created:
#             like.delete()
#             liked = False
#         else:
#             liked = True
        
#         # Update like count
        post.likes_count = post.likes.count()
        post.save()
        
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes_count
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def bookmark_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            bookmark.delete()
            bookmarked = False
        else:
            bookmarked = True
        
        return JsonResponse({'bookmarked': bookmarked})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    posts = Post.objects.filter(author=user, status='published')
    
    # Check if current user follows this user
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'blog/user_profile.html', context)

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'blog/edit_profile.html', {'form': form})

@login_required
def follow_user(request, username):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, username=username)
        
        if user_to_follow != request.user:
            follow, created = Follow.objects.get_or_create(
                follower=request.user, 
                following=user_to_follow
            )
            
            if not created:
                follow.delete()
                following = False
            else:
                following = True
            
            # Update follower counts
            follower_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            following_profile, _ = UserProfile.objects.get_or_create(user=user_to_follow)
            
            follower_profile.following_count = request.user.following.count()
            following_profile.followers_count = user_to_follow.followers.count()
            
            follower_profile.save()
            following_profile.save()
            
            return JsonResponse({'following': following})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Log the user in
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('post__author')
    
    context = {
        'bookmarks': bookmarks,
    }
    return render(request, 'blog/bookmarks.html', context)