"""
Models for the gender analysis web app.
"""
from django.db import models
from .fields import LowercaseCharField


class Pronoun(models.Model):
    """
    A model that allows users to define an individual pronoun and its type
    (e.g. subject, object, reflexive, etc). Pronouns are case-insensitive and will be
    converted to lowercase.
    """
    PRONOUN_TYPES = [
        ('subj', 'Subject'),
        ('obj', 'Object'),
        ('pos_det', 'Possessive determiner'),
        ('pos_pro', 'Possessive pronoun'),
        ('reflex', 'Reflexive'),
    ]

    identifier = LowercaseCharField(max_length=40)
    type = models.CharField(max_length=7, choices=PRONOUN_TYPES)

    def __repr__(self):
        return f'Pronoun({self.identifier, self.type})'

    def __str__(self):
        return f'Pronoun: {self.identifier}\nType: {self.get_type_display()}'

    def __eq__(self, other):
        return self.identifier == other.identifier


class Document(models.Model):
    """
    This model will hold the full text and
    metadata (author, title, publication date, etc.) of a document
    """
    author = models.CharField(max_length=255, blank=True)
    year = models.IntegerField(null=True, blank=True)
    new_attributes = models.JSONField(null=True, blank=True, default=dict)
    text = models.TextField(blank=True)
    title = models.CharField(max_length=255, blank=True)
    word_count = models.PositiveIntegerField(blank=True, null=True, default=None)
    tokenized_text = models.JSONField(null=True, blank=True, default=None)
    word_counts_counter = models.JSONField(null=True, blank=True, default=dict)
    part_of_speech_tags = models.JSONField(null=True, blank=True, default=list)
