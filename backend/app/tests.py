"""
Tests for the main app.
"""

from django.test import TestCase
from .models import Document
from .analysis import document


class MainTests(TestCase):
    """
    Backend TestCase
    """
    # def setUp(self):
    #     super().setUp()
    #     do any setup here

    def test_get_tokenized_text(self):
        doc_1 = Document(text='The quick brown fox jumped over the lazy dog.')
        doc_1.save()
        tokenized_text_1 = ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']
        doc_2 = Document(text="She really likes to eat chocolate!")
        doc_2.save()
        tokenized_text_2 = ['she', 'really', 'likes', 'to', 'eat', 'chocolate']
        self.assertEqual(document.get_tokenized_text(doc_1), tokenized_text_1)
        self.assertEqual(document.get_tokenized_text(doc_2), tokenized_text_2)

    def test_word_count(self):
        doc_1 = Document(text='The quick brown fox jumped over the lazy dog.')
        doc_1.save()
        word_count_1 = 9
        doc_2 = Document(text="She really likes to eat chocolate!")
        doc_2.save()
        word_count_2 = 6
        self.assertEqual(document.word_count(doc_1), word_count_1)
        self.assertEqual(document.word_count(doc_2), word_count_2)

    def test_sample(self):
        """
        Remove me once we have real tests here.
        """
        two = 2
        another_two = 2
        self.assertEqual(two + another_two, 4)
