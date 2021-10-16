from django.urls import path
from . import views


app_name = 'search'

urlpatterns = [
    path(
        'categories/',
        views.SearchCategoryAPIView.as_view(),
        name='search-category'
        )
]
