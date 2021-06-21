"""
Tests for the main app.
"""

from django.test import TestCase
from .models import (
    Pronoun,
)


class PronounTestCase(TestCase):
    """
    TestCase for the Pronoun model
    """

    def setUp(self):
        he = Pronoun(pronoun='he', pronoun_type='subj')
        him = Pronoun(pronoun='him', pronoun_type='obj')
        his = Pronoun(pronoun='his', pronoun_type='pos_det')
        his_2 = Pronoun(pronoun='his', pronoun_type='pos_pro')
        himself = Pronoun(pronoun='himself', pronoun_type='reflex')


class LowercaseCharFieldTestCase(TestCase):
    """
    TestCase for the LowercaseCharField field.
    """


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
