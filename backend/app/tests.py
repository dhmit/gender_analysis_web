"""
Tests for the main app.
"""

from django.test import TestCase
from collections import Counter
from .models import Document


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
        self.assertEqual(doc_1.get_tokenized_text(), tokenized_text_1)
        self.assertEqual(doc_2.get_tokenized_text(), tokenized_text_2)

    def test_get_word_count(self):
        doc_1 = Document(text='The quick brown fox jumped over the lazy dog.')
        doc_1.save()
        word_count_1 = 9
        doc_2 = Document(text='She really likes to eat chocolate!')
        doc_2.save()
        word_count_2 = 6
        self.assertEqual(doc_1.get_word_count(), word_count_1)
        self.assertEqual(doc_2.get_word_count(), word_count_2)

    def test_get_wordcount_counter(self):
        doc_1 = Document(text='Do you like ice cream as much as I do?')
        doc_1.save()
        counter_1 = Counter({'do': 2, 'you': 1, 'like': 1, 'ice': 1, 'cream': 1, 'as': 2, 'much': 1, 'i': 1})
        doc_2 = Document(text='She really likes to eat chocolate!')
        doc_2.save()
        counter_2 = Counter({'she': 1, 'really': 1, 'likes': 1, 'to': 1, 'eat': 1, 'chocolate': 1})
        self.assertEqual(doc_1.get_wordcount_counter(), counter_1)
        self.assertEqual(doc_2.get_wordcount_counter(), counter_2)

    def test_clean_quotes(self):
        doc_1 = Document(text='This is a “smart” phrase')
        doc_1.save()
        cleaned_1 = 'This is a "smart" phrase'
        self.assertEqual(doc_1._clean_quotes(), cleaned_1)

    def test_find_quoted_text(self):
        doc_1 = Document(text='"This is a quote." There is more. "This is my quote."')
        doc_1.save()
        quoted_text_1 = ['"This is a quote."', '"This is my quote."']
        self.assertEqual(doc_1.find_quoted_text(), quoted_text_1)
