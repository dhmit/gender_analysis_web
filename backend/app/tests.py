"""
Tests for the main app.
"""

from django.test import TestCase
from collections import Counter
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
        doc_2 = Document(text='She really likes to eat chocolate!')
        doc_2.save()
        tokenized_text_2 = ['she', 'really', 'likes', 'to', 'eat', 'chocolate']
        self.assertEqual(document.get_tokenized_text(doc_1), tokenized_text_1)
        self.assertEqual(document.get_tokenized_text(doc_2), tokenized_text_2)

    def test_word_count(self):
        doc_1 = Document(text='The quick brown fox jumped over the lazy dog.')
        doc_1.save()
        word_count_1 = 9
        doc_2 = Document(text='She really likes to eat chocolate!')
        doc_2.save()
        word_count_2 = 6
        self.assertEqual(document.word_count(doc_1), word_count_1)
        self.assertEqual(document.word_count(doc_2), word_count_2)

    def test_get_word_counts_counter(self):
        doc_1 = Document(text='Do you like ice cream as much as I do?')
        doc_1.save()
        counter_1 = Counter({'do': 2, 'you': 1, 'like': 1, 'ice': 1, 'cream': 1, 'as': 2, 'much': 1, 'i': 1})
        doc_2 = Document(text='She really likes to eat chocolate!')
        doc_2.save()
        counter_2 = Counter({'she': 1, 'really': 1, 'likes': 1, 'to': 1, 'eat': 1, 'chocolate': 1})
        self.assertEqual(document.get_wordcount_counter(doc_1), counter_1)
        self.assertEqual(document.get_wordcount_counter(doc_2), counter_2)
