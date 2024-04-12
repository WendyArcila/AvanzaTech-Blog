from django.urls import path
from ..views import UserCreateView, UserLoginView, UserLogoutView


urlpatterns = [
    path('login/', view=UserLoginView.as_view(), name='login'),
    path('logout/', view=UserLogoutView.as_view(), name='logout'),
    path('signup/', view=UserCreateView.as_view(), name='signup')
]
