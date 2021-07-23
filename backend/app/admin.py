"""
This file controls the administrative interface for gender analysis web app.
"""

from django.contrib import admin
from . import models

models_to_register = [
    models.Document,
    models.PronounSeries,
    models.Gender,
    models.Corpus,
    models.ProximityAnalysis,
    models.FrequencyAnalysis,
]

for model in models_to_register:
    admin.site.register(model)
