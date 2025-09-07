from django.db import models
from django_enumfield.enum import EnumField

from ai.enums import Sentiment


class StructuredInfo(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)  # type: ignore
    summary = models.TextField(null=True, blank=True)  # type: ignore
    sentiment = EnumField(Sentiment, null=True, blank=True)  # type: ignore
    topics = models.JSONField(null=True, blank=True)  # type: ignore
    keywords = models.JSONField(null=True, blank=True)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)  # type: ignore

    def __str__(self):
        return f"StructuredInfo(id={self.id}, title={self.title})"
