from django.urls import path
from blog_post.views import BlogPostListCreate

urlpatterns = [
    path('', BlogPostListCreate.as_view(), name='blogpost-create'),
]