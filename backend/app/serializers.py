"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
# import json
from rest_framework import serializers
from .models import (
    Document,
)


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializes a Document object
    """
    class Meta:
        model = Document
        fields = ['id', 'author', 'title', 'date', 'text', 'word_count']
