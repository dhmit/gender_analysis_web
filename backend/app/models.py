"""
Models for the ***** app.
"""
from django.db import models

# no models yet -- write me!

class Document(models.Model):
    """
    This model will hold the full text and
    metadata (author, title, publication date, etc.) of a document
    """
    author = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    date = models.IntegerField(null=True, blank=True)
    text = models.TextField(blank=True)
    label = models.CharField(max_length=255, blank=True)
    _word_counts_counter = models.JSONField(null=True, blank=True, default=dict)
    _word_count = models.PositiveIntegerField(blank=True, null=True, default=None)
    _tokenized_text = models.JSONField(null=True, blank=True, default=list)
    _part_of_speech_tags = models.JSONField(null=True, blank=True, default=list)

