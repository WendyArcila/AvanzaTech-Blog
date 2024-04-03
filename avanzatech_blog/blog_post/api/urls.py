from django.urls import path
from blog_post.views import BlogPostListCreate, BlogPostRetrieveUpdateDeleteView

urlpatterns = [
    path('', BlogPostListCreate.as_view(), name='blogpost-create-list'),
    path('<int:pk>/', BlogPostRetrieveUpdateDeleteView.as_view(), name = 'blogpost-id')
]