from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('shortener', views.ShortenerView.as_view(), name='shortener'),
    path('shortener/<int:shortener_id>', views.ShortenerView.as_view(), name='shortener'),
    path('shortener/search', views.Search.as_view(), name='search'),
    path('shortener/expired', views.ShortenerPurge.as_view(), name='shortener'),
    # matches everything so that we can make thes shortest possible url. Make sure nothing but shortner keys make it to this point.
    re_path(r"^(?P<short_key>[0-9a-zA-Z]+(,[0-9a-zA-Z]+)*)$", views.Redirect.as_view()) 
]

