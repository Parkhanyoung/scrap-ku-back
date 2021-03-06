from django.urls import path
from . import views


app_name = 'search'

urlpatterns = [
    path(
        'courdiv/',
        views.SearchCourdivAPIView.as_view(),
        name='search-courdiv'
        ),
    path(
        'college/',
        views.SearchCollegeAPIView.as_view(),
        name='search-college'
        ),
    path(
        'group/',
        views.SearchGroupAPIView.as_view(),
        name='search-group'
        ),
    path(
        'dept/',
        views.SearchDeptAPIView.as_view(),
        name='search-dept'
        ),
    path(
        'course/',
        views.SearchCourseAPIView.as_view(),
        name='search-course'
        ),
    path(
        'course/<int:pk>/',
        views.RetrieveCourseAPIView.as_view(),
        name='retrieve-course'
        ),
]
