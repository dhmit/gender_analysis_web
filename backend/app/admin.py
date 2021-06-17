"""
This file controls the administrative interface for gender analysis web app
"""

from django.contrib import admin
from . import models

#defining models 
modelsToRegister = [models.PronounSeries, models.Gender]

admin.site.register(models)
