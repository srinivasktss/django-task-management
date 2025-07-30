from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.create_user, name='create_user'),
    path('login/', views.login, name='login'),
    path('user_info/', views.get_user_info, name='user_info'),
]