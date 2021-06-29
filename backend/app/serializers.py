"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
# import json
from rest_framework import serializers
from .models import (
    PronounSeries,
    Document,
)


class PronounSeriesSerializer(serializers.ModelSerializer):
    """
    Serializes a PronounSeries object
    """

    class Meta:
        model = PronounSeries
        fields = ['identifier', 'subj', 'obj', 'pos_det', 'pos_pro', 'reflex']


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializes a Document object
    """

    class Meta:
        model = Document
        fields = ['id', 'author', 'title', 'year', 'text', 'word_count']
