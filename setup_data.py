import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aadiz_blozzers.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, UserProfile

def create_sample_data():
    # Create categories
    categories = [
        {'name': 'Technology', 'description': 'Tech-related posts', 'color': '#007bff'},
        {'name': 'Travel', 'description': 'Travel experiences', 'color': '#28a745'},
        {'name': 'Food', 'description': 'Food and recipes', 'color': '#ffc107'},
        {'name': 'Education', 'description': 'Educational content', 'color': '#6f42c1'},
    ]
    
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"Created category: {category.name}")
    
    # Create tags
    tags = [
        {'name': 'Nepal', 'color': '#dc3545'},
        {'name': 'Digital', 'color': '#17a2b8'},
        {'name': 'Innovation', 'color': '#6c757d'},
        {'name': 'Culture', 'color': '#fd7e14'},
        {'name': 'Adventure', 'color': '#20c997'},
    ]
    
    for tag_data in tags:
        tag, created = Tag.objects.get_or_create(
            name=tag_data['name'],
            defaults=tag_data
        )
        if created:
            print(f"Created tag: {tag.name}")
    
    # Create users with Nepali names
    users_data = [
        {'username': 'binod_panthy', 'first_name': 'Binod', 'last_name': 'Panthy', 'email': 'binod@example.com'},
        {'username': 'aaditya_nepali', 'first_name': 'Aaditya', 'last_name': 'Nepali', 'email': 'aaditya@example.com'},
        {'username': 'anmol_gurung', 'first_name': 'Anmol', 'last_name': 'Gurung', 'email': 'anmol@example.com'},
        {'username': 'barbi_shrestha', 'first_name': 'Barbi', 'last_name': 'Shrestha', 'email': 'barbi@example.com'},
    ]
    
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {user.username}")
            
            # Create profile
            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f"Hello, I'm {user.first_name}! Welcome to my profile.",
                    'location': 'Kathmandu, Nepal'
                }
            )
    
    # Create sample posts
    posts_data = [
        {
            'title': 'The Digital Revolution in Nepal',
            'excerpt': 'How technology is making life easier in Nepal',
            'content': 'The digital revolution has brought significant changes to people\'s lives in Nepal. From mobile banking to online education, technology has made our daily lives easier.',
            'author': 'binod_panthy',
            'category': 'Technology',
            'tags': ['Nepal', 'Digital', 'Innovation']
        },
        {
            'title': 'Beauty of the Himalayas',
            'excerpt': 'The unique beauty of Nepal\'s Himalayan regions',
            'content': 'Nepal\'s Himalayan regions have become a center of attraction for tourists from around the world. From Everest to Annapurna, the mountains here fascinate nature lovers.',
            'author': 'aaditya_nepali',
            'category': 'Travel',
            'tags': ['Nepal', 'Adventure']
        },
        {
            'title': 'Taste of Nepali Cuisine',
            'excerpt': 'Features of traditional Nepali food',
            'content': 'Nepali cuisine has its own special identity. From dal bhat to momo, our traditional foods have fascinated foreigners as well.',
            'author': 'anmol_gurung',
            'category': 'Food',
            'tags': ['Nepal', 'Culture']
        },
        {
            'title': 'Innovation in Education',
            'excerpt': 'Improvements in Nepal\'s education sector',
            'content': 'There have been significant improvements in Nepal\'s education sector recently. From digital education to vocational training, various innovations have improved the quality of education.',
            'author': 'barbi_shrestha',
            'category': 'Education',
            'tags': ['Nepal', 'Innovation']
        }
    ]
    
    for post_data in posts_data:
        author = User.objects.get(username=post_data['author'])
        category = Category.objects.get(name=post_data['category'])
        
        post, created = Post.objects.get_or_create(
            title=post_data['title'],
            defaults={
                'excerpt': post_data['excerpt'],
                'content': post_data['content'],
                'author': author,
                'category': category,
                'status': 'published'
            }
        )
        
        if created:
            # Add tags
            for tag_name in post_data['tags']:
                tag = Tag.objects.get(name=tag_name)
                post.tags.add(tag)
            
            print(f"Created post: {post.title}")
    
    print("\nSample data created successfully!")
    print("You can now login with:")
    print("Username: binod_panthy, Password: password123")
    print("Username: aaditya_nepali, Password: password123")
    print("Username: anmol_gurung, Password: password123")
    print("Username: barbi_shrestha, Password: password123")

if __name__ == '__main__':
    create_sample_data()