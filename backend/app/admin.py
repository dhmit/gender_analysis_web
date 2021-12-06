"""
This file controls the administrative interface for gender analysis web app.
"""

from django.contrib import admin
from . import models

from .models import Corpus, DistinctivenessAnalysis


class CorpusAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')


class DistinctivenessAdmin(admin.ModelAdmin):
    list_display = ('pk', 'corpus_1_id', 'corpus_2_id')


models_to_register = [
    models.Document,
    models.PronounSeries,
    models.Gender,
    models.ProximityAnalysis,
    models.FrequencyAnalysis,
]

for model in models_to_register:
    admin.site.register(model)

admin.site.register(Corpus, CorpusAdmin)
admin.site.register(DistinctivenessAnalysis, DistinctivenessAdmin)

