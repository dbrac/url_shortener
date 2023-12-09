from django.db import models
from django.conf import settings


class Shortener(models.Model):
    DURATIONS = {
        "1": "1",
        "3": "3",
        "6": "6",
        "12": "12"
    }
    url = models.TextField(max_length=300)
    short_key = models.TextField(max_length=30)
    tags = models.TextField(max_length=100)
    active_duration = models.CharField(max_length=2, choices=DURATIONS)
    createdDate = models.DateTimeField(auto_now_add=True)

