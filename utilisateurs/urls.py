# users/urls.py
from django.urls import path
from .views import LoginAPIView, LogoutAPIView
from . import views
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
     path('profile/', views.user_profile, name='user_profile'),
]
