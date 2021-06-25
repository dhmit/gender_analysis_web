"""
Custom managers for the gender analysis web app.
"""
from django.db import models


class DocumentManager(models.Manager):
    def create_document(self, **attributes):
        doc = self.create(**attributes)
        doc.get_tokenized_text_wc_and_pos()
        return doc
