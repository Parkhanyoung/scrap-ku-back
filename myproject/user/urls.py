from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('users/', views.UserCreateAPIView.as_view(), name='user-list'),
    path('users/me/', views.UserManageAPIView.as_view(), name='user-me')
]
