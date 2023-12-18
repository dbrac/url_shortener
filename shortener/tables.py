import django_tables2 as tables
from .models import Shortener
from django_tables2.utils import A

class ShortenerResultsTable(tables.Table):
    class Meta:
        model = Shortener
        # template_name = "django_tables2/bootstrap.html"
        fields = ('short_key', 'url', 'tags', 'createdDate')
        attrs = {"class": "table table-striped table-sm table-bordered mt-5"}
        orderable = False
        # short_key = tables.TemplateColumn('<a href="https://www.google.com">{{ shortener_results.short_key }}</a>')
        buttons = tables.TemplateColumn(
            template_name="shortener/templates/search.html", verbose_name=("actions"), orderable=False
        )
