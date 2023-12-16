from django.urls import path
from . import views

# app_name = shortener

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('search/', views.Search.as_view(), name='search'),
    path(r'^<short_key>', views.Redirect.as_view())
]