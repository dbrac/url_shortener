from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('shortener/<int:shortener_id>', views.ShortenerView.as_view(), name='shortener'),
    path('shortener', views.ShortenerView.as_view(), name='shortener'),
    path('search', views.Search.as_view(), name='search'),
    re_path(r"^(?P<short_key>[0-9a-zA-Z]+(,[0-9a-zA-Z]+)*)$", views.Redirect.as_view())
]
