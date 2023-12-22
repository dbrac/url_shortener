from django.db import models
from django.conf import settings


class Shortener(models.Model):
    DURATIONS = {
        "1": "1 month",
        "3": "3 months",
        "6": "6 months",
        "12": "12 months"
    }
    url = models.URLField(max_length=300)
    short_key = models.CharField(max_length=30)
    tags = models.CharField(max_length=100, blank=True)
    active_duration = models.CharField(max_length=2, choices=DURATIONS)
    createdDate = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.short_key} -> {self.url}"
