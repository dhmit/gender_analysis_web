"""
Models for the gender analysis web app.
"""
from django.db import models
from .fields import LowercaseCharField


class Pronoun(models.Model):
    """
    A model that allows users to define an individual pronoun and its type
    (e.g. subject, object, reflexive, etc). Pronouns are case-insensitive and will be
    converted to lowercase.
    """
    PRONOUN_TYPES = [
        ('subj', 'Subject'),
        ('obj', 'Object'),
        ('pos_det', 'Possessive determiner'),
        ('pos_pro', 'Possessive pronoun'),
        ('reflex', 'Reflexive'),
    ]

    pronoun = LowercaseCharField(max_length=40)
    pronoun_type = models.CharField(max_length=7, choices=PRONOUN_TYPES)

    def __repr__(self):
        return f'Pronoun({self.pronoun, self.pronoun_type})'

    def __str__(self):
        pronoun_type_str = ''

        for PRONOUN_TYPE in Pronoun.PRONOUN_TYPES:
            if PRONOUN_TYPE[0] == self.pronoun_type:
                pronoun_type_str = PRONOUN_TYPE[1]
                break

        return (
            f'Pronoun: {self.pronoun}\nType: {pronoun_type_str}'
        )
