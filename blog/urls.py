from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and posts
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    
    
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # User profiles
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),

    # AJAX endpoints
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('bookmark/<int:pk>/', views.bookmark_post, name='bookmark_post'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    
    # User features
    path('bookmarks/', views.my_bookmarks, name='my_bookmarks'),
]