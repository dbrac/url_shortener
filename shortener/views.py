from django.shortcuts import render
from django.views import View
from shortener.models import Shortener
from .forms import ShortenerForm, SearchForm, UpdateShortenerForm
from django.contrib import messages
from .models import Shortener
from django.shortcuts import redirect
from django.utils.timezone import make_aware
# from datetime import datetime, timedelta
import datetime

class Index(View):

    # render index form used for create
    def get(self, request):
        form = ShortenerForm
        return render(request, 'index.html', {"form": form})


class Search(View):

    # render search form
    def get(self, request):
        form = SearchForm
        return render(request, 'search.html', {"form": form})


class ShortenerView(View):
    # handles the form actions for retrieving and modifying shortener's

    # list
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
            if request.GET["created_before"]:
                date = request.GET.get('created_before', '').split('-')
                args["createdDate__lt"] = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            if request.GET["created_after"]:
                date = request.GET.get('created_after', '').split('-')
                args["createdDate__gt"] = datetime.date(int(date[0]), int(date[1]), int(date[2]))

            shortener_results = None
            if len(args) > 0:
                shortener_results = Shortener.objects.filter(**args)
            else:
                messages.success(request, 'No Results!')

            if shortener_results:
                return render(request, 'search.html', {"form": form, "shortener_queryset": shortener_results})
            else:
                return render(request, 'search.html', {"form": form})

        # GET - renders the update shortener form
        else:
            shortener_record = Shortener.objects.get(pk=shortener_id)
            form = UpdateShortenerForm({
                "short_key": shortener_record.short_key,
                "url": shortener_record.url,
                "tags": shortener_record.tags,
                "expires": shortener_record.expires.strftime("%Y-%m-%d") if shortener_record else None # shouldn't run into this any more
            })
            return render(request, 'update.html', {"form": form})


    def post(self, request):
        form = ShortenerForm
        if request.POST["formaction"] == "create":
            form = ShortenerForm(request.POST)
            valid = form.is_valid()
            if form.is_valid():
                # fake save so we can modify before writing to db
                form = form.save(commit=False)
                expires = datetime.datetime.today() + datetime.timedelta(int(request.POST["active_duration"])*365/12)
                form.expires = make_aware(expires)
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
                "expires": shortener_record.expires.strftime("%Y-%m-%d")
            })
            return render(request, 'update.html', {"form": form})

        if request.POST["formaction"] == "delete":
            shortener_record = Shortener.objects.get(short_key__iexact=request.POST["short_key"])
            messages.success(request, 'Shortener Deleted!')
            form = UpdateShortenerForm({
                "short_key": shortener_record.short_key,
                "url": shortener_record.url,
                "tags": shortener_record.tags,
                "expires": shortener_record.expires.strftime("%Y-%m-%d")
            })
            shortener_record.delete()
            return render(request, 'update.html', {"form": form})


class Redirect(View):
    # only implemented get. intended use is for users web browsers and not applications.
    def get(self, request, short_key):
        shortener_results = Shortener.objects.get(short_key__iexact=short_key)
        shortener_results.hits += 1
        shortener_results.save()
        return redirect(shortener_results.url)


