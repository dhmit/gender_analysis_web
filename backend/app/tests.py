"""
Tests for the gender analysis web app.
"""
from collections import Counter
from django.test import TestCase
from .models import (
    Document,
)


class DocumentTestCase(TestCase):
    """
    Test cases for the Document model
    """

    def setUp(self):
        Document.objects.create_document(title='doc1', year=2021, text='The quick brown fox jumped over the lazy dog.')
        Document.objects.create_document(title='doc2', text='She really likes to eat chocolate!')
        Document.objects.create_document(title='doc3', text='Do you like ice cream as much as I do?')
        Document.objects.create(title='doc4', text='This is a ‘very’ “smart” phrase')
        Document.objects.create_document(title='doc5', text='"This is a quote." There is more. "This is my quote."')
        Document.objects.create_document(title='doc6', text="""She took a lighter out of her purse and handed it over to him.
                                 He lit his cigarette and took a deep drag from it, and then began
                                 his speech which ended in a proposal. Her tears drowned the ring.""")
        Document.objects.create_document(title='doc7', text="""Hester was convicted of adultery. which made her very sad,
                                 and then Arthur was also sad, and everybody was sad and then
                                 Arthur died and it was very sad.  Sadness.""")
        Document.objects.create_document(title='doc8', text="""Jane was convicted of adultery. she was a beautiful gal,
                                 and everyone thought that she was very beautiful, and everybody
                                 was sad and then she died. Everyone agreed that she was a beautiful
                                 corpse that deserved peace.""")
        Document.objects.create_document(title='doc9', text='They refuse to permit us to obtain the refuse permit.')

    def test_get_tokenized_text_wc_and_pos(self):
        doc_1 = Document.objects.get(title='doc1')
        tokenized_text_1 = ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']
        doc_2 = Document.objects.get(title='doc2')
        tokenized_text_2 = ['she', 'really', 'likes', 'to', 'eat', 'chocolate']
        counter_2 = Counter({'she': 1, 'really': 1, 'likes': 1, 'to': 1, 'eat': 1, 'chocolate': 1})
        doc_3 = Document.objects.get(title='doc3')
        counter_3 = Counter({'do': 2, 'you': 1, 'like': 1, 'ice': 1, 'cream': 1, 'as': 2, 'much': 1, 'i': 1})
        doc_9 = Document.objects.get(title='doc9')
        tags_1 = [['they', 'PRP'], ['refuse', 'VBP'], ['to', 'TO'], ['permit', 'VB']]
        tags_2 = [['obtain', 'VB'], ['the', 'DT'], ['refuse', 'NN'], ['permit', 'NN']]
        self.assertEqual(doc_1.tokenized_text, tokenized_text_1)
        self.assertEqual(doc_1.word_count, 9)
        self.assertEqual(doc_2.tokenized_text, tokenized_text_2)
        self.assertEqual(doc_2.word_count, 6)
        self.assertEqual(doc_2.word_count_counter, counter_2)
        self.assertEqual(doc_3.word_count_counter, counter_3)
        self.assertEqual(doc_9.part_of_speech_tags[:4], tags_1)
        self.assertEqual(doc_9.part_of_speech_tags[-4:], tags_2)

    def test_clean_quotes(self):
        doc = Document.objects.get(title='doc4')
        cleaned = 'This is a \'very\' "smart" phrase'
        self.assertEqual(doc._clean_quotes(), cleaned)

    def test_find_quoted_text(self):
        doc = Document.objects.get(title='doc5')
        quoted_text = ['"This is a quote."', '"This is my quote."']
        self.assertEqual(doc.find_quoted_text(), quoted_text)

    def test_get_count_of_word(self):
        doc = Document.objects.get(title='doc3')
        self.assertEqual(doc.get_count_of_word('do'), 2)
        self.assertEqual(doc.get_count_of_word('ThisWordIsNotThere'), 0)

    def test_get_count_of_words(self):
        doc = Document.objects.get(title='doc3')
        self.assertEqual(doc.get_count_of_words(['do', 'as', 'you']), Counter({'do': 2, 'as': 2, 'you': 1}))
        self.assertEqual(doc.get_count_of_words(['ThisWordIsNotThere', 'well']),
                         Counter({'ThisWordIsNotThere': 0, 'well': 0}))

    def test_words_associated(self):
        doc = Document.objects.get(title='doc6')
        self.assertEqual(doc.words_associated('his'), Counter({'cigarette': 1, 'speech': 1}))

    def test_get_word_windows(self):
        doc = Document.objects.get(title='doc6')
        windows_1 = Counter(
            {'he': 1, 'lit': 1, 'cigarette': 1, 'and': 1, 'then': 1, 'began': 1, 'speech': 1, 'which': 1})
        windows_2 = Counter({'her': 2, 'of': 1, 'and': 1, 'handed': 1, 'proposal': 1, 'drowned': 1, 'the': 1})
        self.assertEqual(doc.get_word_windows('his', window_size=2), windows_1)
        self.assertEqual(doc.get_word_windows(['purse', 'tears']), windows_2)

    def test_get_word_freq(self):
        doc = Document.objects.get(title='doc7')
        self.assertEqual(doc.get_word_freq('sad'), 0.13333333333333333)

    def test_get_word_frequencies(self):
        doc = Document.objects.get(title='doc8')
        word_freqs = {'peace': 0.02702702702702703, 'died': 0.02702702702702703, 'foobar': 0.0}
        self.assertEqual(doc.get_word_freqs(['peace', 'died', 'foobar']), word_freqs)

    def test_part_of_speech_words(self):
        doc = Document.objects.get(title='doc8')
        words = {'JJ': Counter({'beautiful': 3}), 'VBD': Counter({'died': 1}), 'NN': Counter({'peace': 1})}
        self.assertEqual(doc.get_part_of_speech_words(['peace', 'died', 'beautiful', 'foobar']), words)

    def test_update_metadata(self):
        doc = Document.objects.get(title='doc1')
        doc.update_metadata({'year': 1903})
        new_attribute = {'cookies': 'chocolate chip'}
        doc.update_metadata(new_attribute)
        new_attribute_2 = {'text': 'The quick brown fox jumped over the lazy dog.'}
        doc.update_metadata(new_attribute_2)
        self.assertEqual(doc.year, 1903)
        self.assertEqual(doc.new_attributes['cookies'], 'chocolate chip')
        self.assertEqual(doc.word_count, 9)


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

    def test_get_count_of_word(self):
        doc_1 = Document(text='Do you like ice cream as much as I do?')
        doc_1.save()
        self.assertEqual(doc_1.get_count_of_word('do'), 2)
        self.assertEqual(doc_1.get_count_of_word('ThisWordIsNotThere'), 0)

    def test_get_count_of_words(self):
        doc_1 = Document(text='Do you like ice cream as much as I do?')
        doc_1.save()
        self.assertEqual(doc_1.get_count_of_words(['do', 'as', 'you']), Counter({'do': 2, 'as': 2, 'you': 1}))
        self.assertEqual(doc_1.get_count_of_words(['ThisWordIsNotThere', 'well']), Counter({'ThisWordIsNotThere': 0, 'well': 0}))

    def test_words_associated(self):
        doc_1 = Document(text="""She took a lighter out of her purse and handed it over to him.
                                 He lit his cigarette and took a deep drag from it, and then
                                 began his speech which ended in a proposal. Her tears drowned the ring.
                                 TBH i know nothing about this story.""")
        doc_1.save()
        self.assertEqual(doc_1.words_associated('his'), Counter({'cigarette': 1, 'speech': 1}))

    def test_get_word_windows(self):
        doc_1 = Document(text="""She took a lighter out of her purse and handed it over to him.
                                 He lit his cigarette and took a deep drag from it, and then began
                                 his speech which ended in a proposal. Her tears drowned the ring.""")
        doc_1.save()
        windows_1 = Counter({'he': 1, 'lit': 1, 'cigarette': 1, 'and': 1, 'then': 1, 'began': 1, 'speech': 1, 'which': 1})
        windows_2 = Counter({'her': 2, 'of': 1, 'and': 1, 'handed': 1, 'proposal': 1, 'drowned': 1, 'the': 1})
        self.assertEqual(doc_1.get_word_windows('his', window_size=2), windows_1)
        self.assertEqual(doc_1.get_word_windows(['purse', 'tears']), windows_2)

    def test_get_word_freq(self):
        doc_1 = Document(text="""Hester was convicted of adultery. which made her very sad,
                                 and then Arthur was also sad, and everybody was sad and then
                                 Arthur died and it was very sad.  Sadness.""")
        doc_1.save()
        self.assertEqual(doc_1.get_word_freq('sad'), 0.13333333333333333)

    def test_get_word_frequencies(self):
        doc_1 = Document(text="""Jane was convicted of adultery. she was a beautiful gal,
                                 and everyone thought that she was very beautiful, and everybody
                                 was sad and then she died. Everyone agreed that she was a beautiful
                                 corpse that deserved peace.""")
        doc_1.save()
        word_freqs = {'peace': 0.02702702702702703, 'died': 0.02702702702702703, 'foobar': 0.0}
        self.assertEqual(doc_1.get_word_frequencies(['peace', 'died', 'foobar']), word_freqs)

    def test_get_part_of_speech_tags(self):
        doc_1 = Document(text='They refuse to permit us to obtain the refuse permit.')
        doc_1.save()
        tags_1 = [('They', 'PRP'), ('refuse', 'VBP'), ('to', 'TO'), ('permit', 'VB')]
        tags_2 = [('the', 'DT'), ('refuse', 'NN'), ('permit', 'NN'), ('.', '.')]
        self.assertEqual(doc_1.get_part_of_speech_tags()[:4], tags_1)
        self.assertEqual(doc_1.get_part_of_speech_tags()[-4:], tags_2)

    def test_part_of_speech_words(self):
        doc_1 = Document(text="""Jane was convicted of adultery. she was a beautiful gal,
                                         and everyone thought that she was very beautiful, and everybody
                                         was sad and then she died. Everyone agreed that she was a beautiful
                                         corpse that deserved peace.""")
        doc_1.save()
        words = {'JJ': Counter({'beautiful': 3}), 'VBD': Counter({'died': 1}), 'NN': Counter({'peace': 1})}
        self.assertEqual(doc_1.get_part_of_speech_words(['peace', 'died', 'beautiful', 'foobar']), words)

    def test_update_metadata(self):
        doc_1 = Document(date=2098)
        doc_1.save()
        doc_1.update_metadata({'date': '1903'})
        new_attribute = {'cookies': 'chocolate chip'}
        doc_1.update_metadata(new_attribute)
        new_attribute_2 = {'text': 'The quick brown fox jumped over the lazy dog.'}
        doc_1.update_metadata(new_attribute_2)
        self.assertEqual(doc_1.date, 1903)
        self.assertEqual(doc_1.other['cookies'], 'chocolate chip')
        self.assertEqual(doc_1.word_count, 9)
