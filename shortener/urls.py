from django.urls import path
from . import views

# app_name = shortener

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('shortener/<int:shortener_id>', views.ShortenerView.as_view(), name='shortener'),
    path('shortener', views.ShortenerView.as_view(), name='shortener'),
    path('search', views.Search.as_view(), name='search'),
    path('<short_key>', views.Redirect.as_view()),
    #TODO shortener/id (get, put, delete)
    #TODO shortener (list, post)
    #TODO /<short_key> (GET)
    #TODO / (GET) index
]