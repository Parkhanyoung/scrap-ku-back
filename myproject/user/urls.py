from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('users/', views.UserCreateView.as_view(), name='user-list'),
    path('users/me/', views.UserManageView.as_view(), name='user-me'),
    path('users/token/', views.TokenCreateView.as_view(), name='user-token')
]
