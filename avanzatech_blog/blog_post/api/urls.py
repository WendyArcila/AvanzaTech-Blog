from django.urls import path
from blog_post.views import BlogPostListCreate, BlogPostRetrieveUpdateView

urlpatterns = [
    path('', BlogPostListCreate.as_view(), name='blogpost-create-list'),
    path('<int:pk>/', BlogPostRetrieveUpdateView.as_view(), name = 'blogpost-id')
]