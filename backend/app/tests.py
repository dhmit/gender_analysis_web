"""
Tests for the gender analysis web app.
"""

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
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
        Pronoun.objects.create(identifier='he', type='subj')
        Pronoun.objects.create(identifier='him', type='obj')
        Pronoun.objects.create(identifier='his', type='pos_det')
        Pronoun.objects.create(identifier='his', type='pos_pro')
        Pronoun.objects.create(identifier='himself', type='reflex')

        Pronoun.objects.create(identifier='Hiis', type='pos_pro')

    def test_models_save(self):
        he = Pronoun.objects.get(identifier='he')
        self.assertEqual(str(he), 'Pronoun: he\nType: Subject')
        self.assertEqual(type(he.type), str)
        he.save()

        with self.assertRaises(ObjectDoesNotExist):
            # This raises as expected
            should_be_lowercase = Pronoun.objects.get(identifier='Hiis')

            # This does not!
            should_be_lowercase = Pronoun(identifier='Hiis', type='pos_pro')

        # These should be equal (i.e. both identifiers converted to lowercase) but are not!
        # The identifier is not converted to lowercase if creating an object using a regular Python constructor
        self.assertEqual(Pronoun.objects.get(identifier='hiis'), Pronoun(identifier='Hiis', type='pos_pro'))

        his = Pronoun.objects.get(identifier='his', type='pos_det')
        his_2 = Pronoun.objects.get(identifier='his', type='pos_pro')
        self.assertEqual(his, his_2)
        his.save()
        his_2.save()





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
