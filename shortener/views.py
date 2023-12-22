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

    def get(self, request):
        form = ShortenerForm
        return render(request, 'index.html', {"form": form})


class Search(View):

    def get(self, request):
        form = SearchForm
        return render(request, 'search.html', {"form": form})


class ShortenerView(View):

    def get(self, request, shortener_id=None):
        if request.GET.get("formaction", None) == "list":
            form = SearchForm
            args = dict()
            if request.GET["url"]:
                args["url__contains"] = request.GET["url"]
            if request.GET["short_key"]:
                args["short_key__contains"] = request.GET["short_key"]
            if request.GET["tags"]:
                args["tags__contains"] = request.GET["tags"]

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
                                                   "shortener_list": shortener_list,

                                                      "shortener_queryset": shortener_results})
        # GET
        else:
            shortener_record = Shortener.objects.get(pk=shortener_id)
            form = UpdateShortenerForm({
                "short_key": shortener_record.short_key,
                "url": shortener_record.url,
                "tags": shortener_record.tags,
                "active_duration": shortener_record.active_duration
            })
            return render(request, 'update.html', {"form": form})


    def post(self, request):
        form = ShortenerForm
        if request.POST["formaction"] == "create":
            form = ShortenerForm(request.POST)
            valid = form.is_valid()
            if form.is_valid():
                form.save()
                messages.success(request, 'Created Successfully!')
                form = ShortenerForm
            return render(request, 'index.html', {"form": form})

        if request.POST["formaction"] == "update":
            shortener_record = Shortener.objects.get(short_key__iexact=request.POST["short_key"])
            shortener_record.url = request.POST["url"]
            shortener_record.tags = request.POST["tags"]
            shortener_record.save()
            messages.success(request, 'Shortener Updated!')
            form = UpdateShortenerForm({
                "short_key": shortener_record.short_key,
                "url": shortener_record.url,
                "tags": shortener_record.tags,
                "active_duration": shortener_record.active_duration
            })
            return render(request, 'update.html', {"form": form})

        if request.POST["formaction"] == "delete":
            shortener_record = Shortener.objects.get(short_key__iexact=request.POST["short_key"])
            messages.success(request, 'Shortener Deleted!')
            form = UpdateShortenerForm({
                "short_key": shortener_record.short_key,
                "url": shortener_record.url,
                "tags": shortener_record.tags,
                "active_duration": shortener_record.active_duration
            })
            shortener_record.delete()
            return render(request, 'search.html', {"form": form})


class Redirect(View):
    # only implemented get. intended use is for users web browsers and not applications.
    def get(self, request, short_key):
        shortener_results = Shortener.objects.get(short_key__iexact=short_key)
        return redirect(shortener_results.url)


