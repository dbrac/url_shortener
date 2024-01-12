from django import forms
from django.forms import ModelForm, SelectDateWidget, TextInput
from shortener.models import Shortener
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from datetime import datetime, timedelta
import re

class ShortenerForm(ModelForm):
    class Meta:
        model = Shortener
        fields = ["url", "short_key", "tags", "active_duration"]
        # this is used if you just put {{ form }} in your template
        # I ended up not doing this so I specify in the template as form labels how they would be presented
        labels = {
            'short_key': 'https://d.b/',
            'active_duration': 'active for',
            'tags': 'tags'
        }
        widgets = {
            "url": forms.URLInput(attrs={"class": "form-control"}),
            "short_key": forms.TextInput(attrs={"class": "form-control"}),
            "tags": forms.TextInput(attrs={"class": "form-control", "placeholder": "tag, tag, tag (comma separated)"}),
            "active_duration": forms.Select(attrs={"class": "col-sm-8 form-select"})
        }


    # active_duration = forms.ChoiceField(widget=forms.Select(attrs={"class": "col-sm-8 form-select"}),
    #                                     initial="keep active for", choices=Shortener.DURATIONS, required=True)
    acknowledgment = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    def clean_short_key(self):
        short_key = self.cleaned_data['short_key']
        key_lookup = Shortener.objects.filter(short_key__iexact=short_key)
        if len(key_lookup) > 0:
            raise ValidationError("Shortener already exists. Please use a unique name.")
        if not short_key.isalnum():
            raise ValidationError("only alphanumeric values allowed")
        return short_key

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        # TODO allow comma's
        if  len(tags) > 0 and not re.search("^[0-9a-zA-Z]+(,[0-9a-zA-Z]+)*$", tags):
            raise ValidationError("Only alphanumeric values separated by a single comma are allowed. Do not include "
                                  "a trailing comma.")
        return tags

    def clean(self):
        return self.cleaned_data


class UpdateShortenerForm(ShortenerForm):
    class Meta:
        model = Shortener
        fields = ["url", "short_key", "tags"]

    url = forms.URLField(label="url", required=True, widget=forms.URLInput(attrs={"class": "form-control"}))
    tags = forms.CharField(label="tags", required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    expires = forms.DateField(label="expires", required=False, widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}))
    short_key = forms.CharField(label="short key", max_length=30, required=False,
                                widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}))

    def clean_short_key(self):
        return self.data['short_key']

    def clean_tags(self):
        return self.data['tags']

    def clean(self):
        return self.data


class SearchForm(forms.Form):
    this_year = datetime.now().year
    previous_years = datetime.now().year - 1
    # short_key needs to be unique. Either make it the pk or validate it's unique
    url = forms.CharField(label="URL", max_length=250, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    short_key = forms.CharField(label="short key", max_length=30, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    tags = forms.CharField(label="tags", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    # owner = forms.CharField(label="owner", max_length=20, required=False)
    created_before = forms.DateTimeField(label="before", required=False, widget=forms.DateInput(
        format=('%Y-%m-%d'),
        attrs={'class': 'form-control',
               'placeholder': 'Select a date',
               'type': 'date'
              }),)
    created_after = forms.DateTimeField(label="after", required=False, widget=forms.DateInput(
        format=('%Y-%m-%d'),
        attrs={'class': 'form-control',
               'placeholder': 'Select a date',
               'type': 'date'
              }),)
