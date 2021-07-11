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
    Character,
    Alias,
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


class AliasSerializer(serializers.ModelSerializer):
    """
    Serializes an Alias object.
    """

    class Meta:
        model = Alias
        fields = ['name', 'count', 'sanitized_pronoun_rates']


class CharacterSerializer(serializers.ModelSerializer):
    """
    Serializes a Character object.
    """
    aliases = AliasSerializer(many=True, read_only = True)

    class Meta:
        model = Character
        fields = ['common_name', 'count', 'full_name', 'gender', 'aliases']


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializes a Document object
    """
    characters = CharacterSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'author', 'title', 'year', 'text', 'word_count', 'characters']


class SimpleDocumentSerializer(serializers.ModelSerializer):
    """
    Serializes a Document object (does not include the text itself)
    """

    class Meta:
        model = Document
        fields = ['id', 'author', 'title', 'year', 'word_count']