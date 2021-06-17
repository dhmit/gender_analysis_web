"""
Custom fields for the gender analysis web app.
"""
from django.db import models
# from django.utils.translation import gettext_lazy


class LowercaseCharField(models.CharField):
    """
    A subclass of models.CharField that converts the string to lowercase
    when saving the model instance to the database.
    """

    # WORK IN PROGRESS!
    # @property
    # def description(self):
    #     return gettext_lazy(f"String (up to {self.max_length}) \
    #         converted to lowercase upon saving the model instance to the database.")

    def pre_save(self, model_instance, add):
        """
        Preprocesses field data before saving a model instance to the database.
        In this case, converts the data described by the CharField to lowercase.
        """
        chars = getattr(model_instance, self.attname)
        setattr(model_instance, self.attname, chars.lower())

        return super().pre_save(model_instance, add)
