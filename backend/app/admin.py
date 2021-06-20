"""
This file controls the administrative interface for gender_analysis_web app
"""

from django.contrib import admin
from .models import (
    Document
)

admin.site.register(Document)
