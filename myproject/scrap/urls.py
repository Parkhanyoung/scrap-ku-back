from django.urls import path
from scrap import views

app_name = 'scrap'

urlpatterns = [
    path('', views.scrap_main, name='scrap-main'),
    path('colleges/', views.scrap_college, name='scrap-college'),
    path('electivesgroups/', views.scrap_group, name='scrap-group'),
    path('departments/', views.scrap_dept, name='scrap-dept'),
    path('depts/courses/', views.scrap_course_dept, name='scrap-course-dept'),
    path('groups/courses/', views.scrap_course_group, name='scrap-course-group'),
    path('courdivs/courses/', views.scrap_course_cd, name='scrap-course-cd'),
    path('danger/delete/all/data/', views.delete_data, name='delete-data')
]
