"""
Tests for the gender analysis web app.
"""
from collections import Counter

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from .models import (
    PronounSeries,
    Document,
    Corpus,
    Gender,
)
from .analysis import proximity


class PronounSeriesTestCase(TestCase):
    """
    TestCase for the Pronoun model
    """

    def setUp(self):
        PronounSeries.objects.create(
            identifier='Masc_1',
            subj='he',
            obj='him',
            pos_det='his',
            pos_pro='HIS',
            reflex='himself'
        )

        PronounSeries.objects.create(
            identifier='Masc_2',
            subj='HE',
            obj='HIM',
            pos_det='HIS',
            pos_pro='HIS',
            reflex='HIMSELF'
        )

        PronounSeries.objects.create(
            identifier='Fem',
            subj='she',
            obj='her',
            pos_det='her',
            pos_pro='hers',
            reflex='herself'
        )

    def test_PronounSeries_save(self):
        """
        Tests the __str__, __repr__, and __iter__ methods on the PronounSeries model.
        By testing the model's .save() mechanism, this also tests that LowercaseCharField works
        as expected.
        """
        masc_1 = PronounSeries.objects.get(pk=1)
        masc_2 = PronounSeries.objects.get(pk=2)
        self.assertEqual(str(masc_1), 'Masc_1-series')
        self.assertEqual(repr(masc_2), "<Masc_2: ['he', 'him', 'himself', 'his']>")

        with self.assertRaises(ObjectDoesNotExist):
            was_converted_to_lowercase = PronounSeries.objects.get(reflex='HIMSELF')

        has_caps_until_saving = PronounSeries(
            identifier='Masc_2',
            subj='HE',
            obj='HIM',
            pos_det='HIS',
            pos_pro='HIS',
            reflex='HIMSELF'
        )

        self.assertNotEqual(masc_2, has_caps_until_saving)

        has_caps_until_saving.save()
        self.assertEqual(masc_2, has_caps_until_saving)

    def test_PronounSeries_methods(self):
        """
        Tests all other PronounSeries methods explicitly specified in the class not already tested
        in test_PronounSeries_save.
        """
        fem = PronounSeries.objects.get(pk=3)

        self.assertEqual(fem.all_pronouns, {'she', 'her', 'hers', 'herself'})
        self.assertTrue('SHE' in fem)

        should_be_hashable = {fem}


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
            {'he': 1, 'lit': 1, 'cigarette': 1, 'and': 1, 'then': 1, 'began': 1, 'speech': 1, 'which': 1}
        )
        windows_2 = Counter({'her': 2, 'of': 1, 'and': 1, 'handed': 1, 'proposal': 1, 'drowned': 1, 'the': 1})
        windows_3 = Counter({'tears': 1, 'drowned': 1, 'the': 1})
        windows_4 = Counter({'she': 1, 'a': 2, 'lighter': 1, 'cigarette': 1, 'and': 1, 'deep': 1})

        self.assertEqual(doc.get_word_windows('his', window_size=2), windows_1)
        self.assertEqual(doc.get_word_windows(['purse', 'tears']), windows_2)
        self.assertEqual(doc.get_word_windows('ring', window_size=3), windows_3)
        self.assertEqual(doc.get_word_windows('took'), windows_4)

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

class FrequencyTestCase(TestCase):
    """
    Test cases for the frequency analysis
    """



class CorpusTestCase(TestCase):
    """
    Test Cases for the Corpus Model
    """

    def setUp(self):
        Corpus.objects.create(title='corpus1', description='testing corpus save')
        Document.objects.create_document(title='doc1', year=2021, text='The quick brown fox jumped over the lazy dog.')
        Document.objects.create_document(title='doc2', text='She really likes to eat chocolate!')
        Document.objects.create_document(title='doc3', text='Do you like ice cream as much as I do?')

    def test_add_document_to_corpus(self):
        corpus1 = Corpus.objects.get(title='corpus1')
        doc1 = Document.objects.get(title='doc1')
        doc2 = Document.objects.get(title='doc2')
        doc3 = Document.objects.get(title='doc3')
        doc1.corpus_set.add(corpus1)
        self.assertEqual(list(corpus1.documents.all()), [doc1])
        corpus1.documents.add(doc2, doc3)
        self.assertEqual(list(corpus1.documents.all()), [doc1, doc2, doc3])


class ProximityTestCase(TestCase):
    """
    Test Cases for the analysis functions in `proximity.py`
    """

    def setUp(self):
        self.maxDiff = None

        text_1 = "He went to get himself an ice cream, and he also got one for her. She was happy."
        text_2 = """Fairest Cordelia, that art most rich being poor; Most choice, forsaken; and most loved her,
                 despised, herself and himself virtues here I hers hers seize upon. Lear then banishes his daughter
                 to France."""
        text_3 = """She sells seashells by the seashore. He he reads books. She likes math.
                 His father is scared of spiders."""

        Document.objects.create_document(title='Text 1', year=2021, text=text_1)
        Document.objects.create_document(title='Text 2', year=2021, text=text_2)
        Document.objects.create_document(title='Text 3', year=2021, text=text_3)

        corpus = Corpus.objects.create(
            title='Test Corpus',
            description='Testing the analysis functions in `proximity.py`'
        )
        corpus.documents.add(1, 2, 3)

    def test_proximity(self):
        male = Gender.objects.get(pk=1, label='Male')
        female = Gender.objects.get(pk=2, label='Female')
        they = Gender.objects.get(pk=3, label='Nonbinary')
        neo = Gender.objects.get(pk=4, label='Neo')

        #  MALE: (identifier = "Masc",subj = "he",obj = "him",pos_det = "his",pos_pro = "his",reflex = "himself")
        #  FEMALE: (identifier = "Fem",subj = "she",obj = "her",pos_det = "her",pos_pro = "hers",reflex = "herself")

        results = proximity.run_analysis(1, 3)
        expected = {
            # Tagged tokens for text_1: [('he', 'PRP'), ('went', 'VBD'), ('to', 'TO'), ('get', 'VB'),
            # ('himself', 'PRP'), ('an', 'DT'), ('ice', 'NN'), ('cream', 'NN'), ('and', 'CC'), ('he', 'PRP'),
            # ('also', 'RB'), ('got', 'VBD'), ('one', 'CD'), ('for', 'IN'), ('her', 'PRP$'), ('she', 'PRP'),
            # ('was', 'VBD'), ('happy', 'JJ')]
            1: {
                male: {
                    'subj': {'VBD': Counter(['went', 'got']),
                             'TO': Counter(['to']),
                             'VB': Counter(['get']),
                             'NN': Counter(['ice', 'cream']),
                             'CC': Counter(['and']),
                             'RB': Counter(['also']),
                             'CD': Counter(['one']),
                             },
                    'obj': {},
                    'pos_det': {},
                    'pos_pro': {},
                    'reflex': {'VBD': Counter(['went']),
                               'TO': Counter(['to']),
                               'VB': Counter(['get']),
                               'DT': Counter(['an']),
                               'NN': Counter(['ice', 'cream']),
                               }
                },
                female: {
                    'subj': {'PRP$': Counter(['her']),
                             'CD': Counter(['one']),
                             'IN': Counter(['for']),
                             'VBD': Counter(['was']),
                             'JJ': Counter(['happy']),
                             },
                    'obj': {'PRP': Counter(['she']),
                            'VBD': Counter(['got', 'was']),
                            'CD': Counter(['one']),
                            'IN': Counter(['for']),
                            'JJ': Counter(['happy']),
                            },
                    'pos_det': {'PRP': Counter(['she']),
                                'VBD': Counter(['got', 'was']),
                                'CD': Counter(['one']),
                                'IN': Counter(['for']),
                                'JJ': Counter(['happy']),
                                },
                    'pos_pro': {},
                    'reflex': {}
                },
                they: {'subj': {},
                       'obj': {},
                       'pos_det': {},
                       'pos_pro': {},
                       'reflex': {}
                       },
                neo: {'subj': {},
                      'obj': {},
                      'pos_det': {},
                      'pos_pro': {},
                      'reflex': {}
                      }
            },

            # Tagged tokens for text_2: [('fairest', 'JJS'), ('cordelia', 'NN'), ('that', 'IN'), ('art', 'VBZ'),
            # ('most', 'RBS'), ('rich', 'JJ'), ('being', 'VBG'), ('poor', 'JJ'), ('most', 'RBS'), ('choice', 'NN'),
            # ('forsaken', 'VBN'), ('and', 'CC'), ('most', 'JJS'), ('loved', 'VBD'), ('her', 'PRP'),
            # ('despised', 'VBD'), ('herself', 'PRP'), ('and', 'CC'), ('himself', 'PRP'), ('virtues', 'NNS'),
            # ('here', 'RB'), ('i', 'VBP'), ('hers', 'NNS'), ('hers', 'NNS'), ('seize', 'VBP'), ('upon', 'IN'),
            # ('lear', 'JJ'), ('then', 'RB'), ('banishes', 'VBZ'), ('his', 'PRP$'), ('daughter', 'NN'), ('to', 'TO'),
            # ('france', 'VB')]
            2: {
                male: {
                    'subj': {},
                    'obj': {},
                    'pos_det': {'JJ': Counter(['lear']),
                                'RB': Counter(['then']),
                                'VBZ': Counter(['banishes']),
                                'NN': Counter(['daughter']),
                                'TO': Counter(['to']),
                                'VB': Counter(['france']),
                                },
                    'pos_pro': {'JJ': Counter(['lear']),
                                'RB': Counter(['then']),
                                'VBZ': Counter(['banishes']),
                                'NN': Counter(['daughter']),
                                'TO': Counter(['to']),
                                'VB': Counter(['france']),
                                },
                    'reflex': {'VBD': Counter(['despised']),
                               'PRP': Counter(['herself']),
                               'CC': Counter(['and']),
                               'NNS': Counter(['virtues']),
                               'RB': Counter(['here']),
                               'VBP': Counter(['i']),
                               },
                },
                female: {
                    'subj': {},
                    'obj': {'CC': Counter({'and': 2}),
                            'JJS': Counter(['most']),
                            'VBD': Counter(['loved', 'despised']),
                            'PRP': Counter(['herself']),
                            },
                    'pos_det': {'CC': Counter({'and': 2}),
                                'JJS': Counter(['most']),
                                'VBD': Counter(['loved', 'despised']),
                                'PRP': Counter(['herself']),
                                },
                    'pos_pro': {
                        'NNS': Counter(['virtues']),
                        'RB': Counter({'here': 2}),
                        'VBP': Counter({'i': 2, 'seize': 2}),
                        'IN': Counter({'upon': 2}),
                        'JJ': Counter(['lear']),
                    },
                    'reflex': {
                        'PRP': Counter(['her', 'himself']),
                        'VBD': Counter(['loved', 'despised']),
                        'CC': Counter(['and']),
                        'NNS': Counter(['virtues']),
                    },
                },
                they: {'subj': {},
                       'obj': {},
                       'pos_det': {},
                       'pos_pro': {},
                       'reflex': {},
                       },
                neo: {'subj': {},
                      'obj': {},
                      'pos_det': {},
                      'pos_pro': {},
                      'reflex': {},
                      },
            },

            # Tagged tokens for text_3: [('she', 'PRP'), ('sells', 'VBZ'), ('seashells', 'NNS'), ('by', 'IN'),
            # ('the', 'DT'), ('seashore', 'NN'), ('he', 'PRP'), ('he', 'PRP'), ('reads', 'VBZ'), ('books', 'NNS'),
            # ('she', 'PRP'), ('likes', 'VBZ'), ('math', 'NN'), ('his', 'PRP$'), ('father', 'NN'), ('is', 'VBZ'),
            # ('scared', 'VBN'), ('of', 'IN'), ('spiders', 'NNS')]
            3: {
                male: {
                    'subj': {
                        'IN': Counter(['by']),
                        'DT': Counter({'the': 2}),
                        'NN': Counter({'seashore': 2}),
                        'VBZ': Counter({'reads': 2}),
                        'NNS': Counter({'books': 2}),
                        'PRP': Counter(['she']),
                    },
                    'obj': {},
                    'pos_det': {'PRP': Counter(['she']),
                                'VBZ': Counter(['likes', 'is']),
                                'NN': Counter(['math', 'father']),
                                'VBN': Counter(['scared']),
                                },
                    'pos_pro': {'PRP': Counter(['she']),
                                'VBZ': Counter(['likes', 'is']),
                                'NN': Counter(['math', 'father']),
                                'VBN': Counter(['scared']),
                                },
                    'reflex': {},
                },
                female: {
                    'subj': {
                        'VBZ': Counter(['sells', 'reads', 'likes']),
                        'NN': Counter(['math']),
                        'NNS': Counter(['seashells', 'books']),
                        'IN': Counter(['by']),
                        'PRP': Counter(['he']),
                        'PRP$': Counter(['his']),
                    },
                    'obj': {},
                    'pos_det': {},
                    'pos_pro': {},
                    'reflex': {},
                },
                they: {'subj': {},
                       'obj': {},
                       'pos_det': {},
                       'pos_pro': {},
                       'reflex': {},
                       },
                neo: {'subj': {},
                      'obj': {},
                      'pos_det': {},
                      'pos_pro': {},
                      'reflex': {},
                      },
            },
        }

        self.assertEqual(results, expected)
