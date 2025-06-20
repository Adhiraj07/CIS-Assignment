from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegisterView,
    MyTokenObtainPairView,
    UserListView,
    UserDetailView,
    TaskCreateListView,
    TaskDetailView,
    LogoutView
)

urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='register'),
    path('login/',MyTokenObtainPairView.as_view(),name='login'),
    path('token/refresh/',TokenRefreshView.as_view(),name='refresh_token'),
    
    path('users/',UserListView.as_view(),name='user_list'),
    path('users/<int:pk>/',UserDetailView.as_view(),name='user_detail'),
    
    path('tasks/',TaskCreateListView.as_view(),name='task_list'),
    path('tasks/<int:pk>/',TaskDetailView.as_view(),name='task_detail'),
    
    path('logout/',LogoutView.as_view(),name='logout'),
]
