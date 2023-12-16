from django.shortcuts import render
from django.views import View
from shortener.models import Shortener

from .forms import NameForm, ShortenerForm, SearchForm
from django.contrib import messages
from .models import Shortener
from django.shortcuts import redirect

class Index(View):

    def post(self, request):
        form = ShortenerForm(request.POST)
        valid = form.is_valid()
        if form.is_valid():
            form.save()
            messages.success(request, 'Created Successfully!')
            form = ShortenerForm
        return render(request, 'index.html', {"form": form})

    def get(self, request):
        form = ShortenerForm
        return render(request, 'index.html', {"form": form})


class Search(View):

    def get(self, request):
        form = SearchForm
        return render(request, 'search.html', {"form": form})

    # https://django-tables2.readthedocs.io/en/latest/
    def post(self, request):
        form = SearchForm

        args = dict()
        if request.POST["url"]:
            args["url__contains"] = request.POST["url"]
        if request.POST["short_key"]:
            args["short_key__contains"] = request.POST["short_key"]
        if request.POST["tags"]:
            args["tags__contains"] = request.POST["tags"]

        shortener_results = list()
        if len(args) > 0:
            # TODO add date time filters
            shortener_results = list(Shortener.objects.filter(**args).values_list("short_key", "url", "createdDate"))
        else:
            messages.success(request, 'No Results!')

        return render(request, 'search.html', {"form": form, "shortener_results": shortener_results})


class Redirect(View):
    # might want to handle calls other than get
    def get(self, request, short_key):
        shortener_results = Shortener.objects.get(short_key__iexact=short_key)
        return redirect(shortener_results.url)


