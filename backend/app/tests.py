"""
Tests for the gender analysis web app.
"""

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Pronoun,
)


class PronounTestCase(TestCase):
    """
    TestCase for the Pronoun model
    """

    def setUp(self):
        Pronoun.objects.create(identifier='he', type='subj')
        Pronoun.objects.create(identifier='him', type='obj')
        Pronoun.objects.create(identifier='HIS', type='pos_det')
        Pronoun.objects.create(identifier='his', type='pos_pro')
        Pronoun.objects.create(identifier='himself', type='reflex')

    def test_models_save(self):
        he = Pronoun.objects.get(identifier='he')
        self.assertEqual(str(he), 'Pronoun: he\nType: Subject')
        self.assertEqual(type(he.type), str)

        with self.assertRaises(ObjectDoesNotExist):
            was_converted_to_lowercase = Pronoun.objects.get(identifier='HIS')

        his = Pronoun.objects.get(identifier='his', type='pos_det')
        his_caps_until_saving = Pronoun(identifier='HIS', type='pos_pro')
        self.assertNotEqual(his, his_caps_until_saving)

        his_caps_until_saving.save()
        self.assertEqual(his, his_caps_until_saving)


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
