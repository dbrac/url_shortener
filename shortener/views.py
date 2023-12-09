from django.shortcuts import render
from django.views import View
from shortener.models import Shortener


class Index(View):

    def get(self, request):
        return render(request, 'index.html')
