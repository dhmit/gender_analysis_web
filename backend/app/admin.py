"""
This file controls the administrative interface for lang_learn app
"""

from django.contrib import admin
from .models import (
    Document
)

admin.site.register(Document)
