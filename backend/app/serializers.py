"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
# import json
from rest_framework import serializers
from .models import (
    PronounSeries,
    Gender,
    Document,
    Corpus
)


class PronounSeriesSerializer(serializers.ModelSerializer):
    """
    Serializes a PronounSeries object
    """

    class Meta:
        model = PronounSeries
        fields = ['identifier', 'subj', 'obj', 'pos_det', 'pos_pro', 'reflex', 'all_pronouns']


class GenderSerializer(serializers.ModelSerializer):
    """
    Serializes a Gender object
    """
    pronoun_series = PronounSeriesSerializer(read_only=True, many=True)

    class Meta:
        model = Gender
        fields = ['label', 'pronoun_series', 'pronouns', 'subj', 'obj']


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializes a Document object
    """

    class Meta:
        model = Document
        fields = ['id', 'author', 'title', 'year', 'text', 'word_count']


class SimpleDocumentSerializer(serializers.ModelSerializer):
    """
    Serializes a Document object (does not include the text itself)
    """

    class Meta:
        model = Document
        fields = ['id', 'author', 'title', 'year', 'word_count']

class CorpusSerializer(serializers.ModelSerializer):
    """
    Serializes a Corpus object
    """

    class Meta:
        model = Corpus
        fields = ['id', 'title', 'description']