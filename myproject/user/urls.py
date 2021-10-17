from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('', views.UserCreateView.as_view(), name='user-list'),
    path('me/', views.UserManageView.as_view(), name='user-me'),
    path('token/', views.TokenCreateView.as_view(), name='user-token')
]
