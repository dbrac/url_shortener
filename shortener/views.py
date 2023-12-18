from django.shortcuts import render
from django.views import View
from shortener.models import Shortener
from .tables import ShortenerResultsTable
from django_tables2 import SingleTableView

from .forms import NameForm, ShortenerForm, SearchForm, UpdateShortenerForm
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
            # shortener_list = list(Shortener.objects.filter(**args).values_list("short_key", "url", "tags", "createdDate"))
            shortener_list = Shortener.objects.filter(**args).values_list("short_key", "url", "tags", "createdDate")
            shortener_results = Shortener.objects.filter(**args)
            shortener_table = ShortenerResultsTable(shortener_results)
        else:
            messages.success(request, 'No Results!')

        # return render(request, 'search.html', {"form": form, "shortener_results": shortener_results})
        return render(request, 'search.html', {"form": form, "shortener_results": shortener_table,
                                               "shortener_list": shortener_list, "shortener_queryset": shortener_results})


class ShortenerView(View):

    def get(self, request, shortener_id):
        shortener_record = Shortener.objects.get(pk=shortener_id)
        form = UpdateShortenerForm({
            "short_key": shortener_record.short_key,
            "url": shortener_record.url,
            "tags": shortener_record.tags,
            "active_duration": shortener_record.active_duration
        })
        return render(request, 'update.html', {"form": form})

    def delete(self, request, shortener_id):
        form = ShortenerForm
        shortener_record = Shortener.objects.get(pk=shortener_id)
        # shortener_record.delete()
        messages.success(request, 'Shortener Deleted!')
        return render(request, 'search.html', {"form": form} )

    # make put and delet methods then pass in a request type for post, then execute either put or delete. the form actions
    # will call the post with data to decide what to do



class Redirect(View):
    # might want to handle calls other than get
    def get(self, request, short_key):
        shortener_results = Shortener.objects.get(short_key__iexact=short_key)
        return redirect(shortener_results.url)


