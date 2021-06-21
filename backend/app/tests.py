"""
Tests for the main app.
"""

from django.test import TestCase
from .models import (
    Pronoun,
)

from .fields import (
    LowercaseCharField,
)


class PronounTestCase(TestCase):
    """
    TestCase for the Pronoun model
    """

    def setUp(self):
        Pronoun.objects.create(pronoun='he', pronoun_type='subj')
        Pronoun.objects.create(pronoun='him', pronoun_type='obj')
        Pronoun.objects.create(pronoun='his', pronoun_type='pos_det')
        Pronoun.objects.create(pronoun='his', pronoun_type='pos_pro')
        Pronoun.objects.create(pronoun='himself', pronoun_type='reflex')

    def test_models_save(self):
        he = Pronoun.objects.get(pronoun='he')
        he.save()



# class LowercaseCharFieldTestCase(TestCase):
#     """
#     TestCase for the LowercaseCharField field.
#     """
#
#     def setUp(self):
#         foo = LowercaseCharField()


class MainTests(TestCase):
    """
    Backend TestCase
    """

    # def setUp(self):
    #     super().setUp()
    #     do any setup here

    def test_sample(self):
        """
        Remove me once we have real tests here.
        """
        two = 2
        another_two = 2
        self.assertEqual(two + another_two, 4)
