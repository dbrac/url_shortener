from django import forms
from django.forms import ModelForm, SelectDateWidget
from shortener.models import Shortener
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from datetime import datetime

class ShortenerForm(ModelForm):
    class Meta:
        model = Shortener
        fields = ["url", "short_key", "tags", "active_duration"]
        # this is used if you just put {{ form }} in your template
        # I ended up not doing this so I specify in the template as form labels how they would be presented
        labels = {
            'short_key': 'https://d.b/',
            'active_duration': 'keep active for'
        }

    def clean_short_key(self):
        short_key = self.cleaned_data['short_key']
        if not short_key.isalnum():
            raise ValidationError("only alphanumeric values allowed")
        return short_key

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        # TODO allow comma's
        # if not tags.isalnum():
        #     raise ValidationError("only alphanumeric values allowed")
        return tags

    def clean(self):
        # general non field errors
        form_data = self.cleaned_data
        # raise ValidationError("blah")
        return form_data


class SearchForm(forms.Form):
    this_year = datetime.now().year
    previous_years = datetime.now().year - 1
    # short_key needs to be unique. Either make it the pk or validate it's unique
    url = forms.CharField(label="URL", max_length=250, required=False)
    short_key = forms.CharField(label="short key", max_length=30, required=False)
    tags = forms.CharField(label="tags", max_length=100, required=False)
    # owner = forms.CharField(label="owner", max_length=20, required=False)
    created_before = forms.DateTimeField(label="created before", required=False, widget=forms.SelectDateWidget(
        empty_label=("Year", "Month", "Day"), years=range(previous_years, this_year + 1)))
    created_after = forms.DateTimeField(label="created after", required=False, widget=forms.SelectDateWidget(
        empty_label=("Year", "Month", "Day"), years=range(previous_years, this_year + 1)))

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)