"""
Models for the gender analysis web app.
"""
import nltk
import string
import re
from collections import Counter
from more_itertools import windowed
from django.db import models
from .fields import LowercaseCharField
from .managers import DocumentManager


class PronounSeries(models.Model):
    """
    A class that allows users to define a custom series of pronouns to be used in
    analysis functions
    """

    # Things to consider:
    # Add a default to reflex? i.e. default = object pronoun + 'self'?
    # Also, how to we run doctests here? Or use pytest? (configs don't recognize django package or relative filepath
    # in import statement)
    identifier = models.CharField(max_length=60)
    subj = LowercaseCharField(max_length=40)
    obj = LowercaseCharField(max_length=40)
    pos_det = LowercaseCharField(max_length=40)
    pos_pro = LowercaseCharField(max_length=40)
    reflex = LowercaseCharField(max_length=40)

    @property
    def all_pronouns(self):
        """
        :return: The set of all pronoun identifiers.
        """
        pronoun_set = {
            self.subj,
            self.obj,
            self.pos_det,
            self.pos_pro,
            self.reflex,
        }

        return pronoun_set

    def __contains__(self, pronoun):
        """
        Checks to see if the given pronoun exists in this group. This check is case-insensitive
        >>> pronouns = ['They', 'Them', 'Their', 'Theirs', 'Themself']
        >>> pronoun_group = PronounSeries.objects.create('Andy', *pronouns)
        >>> 'they' in pronoun_group
        True
        >>> 'hers' in pronoun_group
        False
        :param pronoun: The pronoun to check for in this group
        :return: True if the pronoun is in the group, False otherwise
        """

        return pronoun.lower() in self.all_pronouns

    def __iter__(self):
        """
        Allows the user to iterate over all of the pronouns in this group. Pronouns
        are returned in lowercase and order is not guaranteed.
        >>> pronouns = ['she', 'her', 'her', 'hers', 'herself']
        >>> pronoun_group = PronounSeries.objects.create('Fem', *pronouns)
        >>> sorted(pronoun_group)
        ['her', 'hers', 'herself', 'she']
        """

        yield from self.all_pronouns

    def __repr__(self):
        """
        >>> PronounSeries.objects.create(
        ...     identifier='Masc',
        ...     subj='he',
        ...     obj='him',
        ...     pos_det='his',
        ...     pos_pro='his',
        ...     reflex='himself'
        ... )
        <Masc: ['he', 'him', 'himself', 'his']>
        :return: A console-friendly representation of the pronoun series
        """

        return f'<{self.identifier}: {list(sorted(self))}>'

    def __str__(self):
        """
        >>> str(PronounSeries.objects.create('Andy', *['Xe', 'Xem', 'Xis', 'Xis', 'Xemself']))
        'Andy-series'
        :return: A string-representation of the pronoun series
        """

        return self.identifier + '-series'

    def __hash__(self):
        """
        Makes the `PronounSeries` class hashable
        """

        return self.identifier.__hash__()

    def __eq__(self, other):
        """
        Determines whether two `PronounSeries` are equal. Note that they are only equal if
        they have the same identifier and the exact same set of pronouns.

        >>> fem_series = PronounSeries.objects.create(
        ...     identifier='Fem',
        ...     subj='she',
        ...     obj='her',
        ...     pos_det='her',
        ...     pos_pro='hers',
        ...     reflex='herself'
        ... )
        >>> second_fem_series = PronounSeries.objects.create(
        ...     identifier='Fem',
        ...     subj='she',
        ...     obj='her',
        ...     pos_pro='hers',
        ...     reflex='herself'
        ...     pos_det='HER',
        ... )
        >>> fem_series == second_fem_series
        True
        >>> masc_series = PronounSeries.objects.create(
        ...     identifier='Masc',
        ...     subj='he',
        ...     obj='him',
        ...     pos_det='his',
        ...     pos_pro='his',
        ...     reflex='himself'
        ... )
        >>> fem_series == masc_series
        False
        :param other: The `PronounSeries` object to compare
        :return: `True` if the two series are the same, `False` otherwise.
        """

        return (
                self.identifier == other.identifier
                and sorted(self) == sorted(other)
        )


class Gender(models.Model):
    """
    This model defines a gender that analysis functions will use to operate.
    """

    label = models.CharField(max_length=60)
    pronoun_series = models.ManyToManyField(PronounSeries)

    def __repr__(self):
        """
        :return: A console-friendly representation of the gender
        >>> Gender('Female')
        <Female>
        """

        return f'<{self.label}>'

    def __str__(self):
        """
        :return: A string representation of the gender
        >>> str(Gender('Female')
        'Female'
        """

        return self.label

    def __hash__(self):
        """
        Allows the Gender object to be hashed
        """

        return self.label.__hash__()

    def __eq__(self, other):
        """
        Performs a check to see whether two `Gender` objects are equivalent. This is true if and
        only if the `Gender` identifiers, pronoun series, and names are identical.

        Note that this comparison works:
        >>> fem_pronouns = PronounSeries.objects.create('Fem', *['she', 'her', 'her', 'hers', 'herself'])

        >>> female = Gender.objects.create('Female')
        >>> female.pronoun_series.add(1)

        >>> another_female = Gender.objects.create('Female')
        >>> another_female.pronoun_series.add(1)

        >>> female == another_female
        True

        But this one does not:
        >>> they_series = PronounSeries.objects.create('They', *['they', 'them', 'their', 'theirs', 'themselves'])
        >>> xe_series = PronounSeries.objects.create('They', *['Xe', 'Xem', 'Xis', 'Xis', 'Xemself'])

        >>> androgynous_1 = Gender.objects.create('NB')
        >>> androgynous_1.pronoun_series.add(2)

        >>> androgynous_2 = Gender.objects.create('NB')
        >>> androgynous_2.pronoun_series.add(3)

        >>> androgynous_1 == androgynous_2
        False
        :param other: The other `Gender` object to compare
        :return: `True` if the `Gender`s are the same, `False` otherwise
        """

        return (
                self.label == other.label
                and list(self.pronoun_series.all()) == list(other.pronoun_series.all())
        )

    @property
    def pronouns(self):
        """
        :return: A set containing all pronouns that this `Gender` uses
        >>> they_series = PronounSeries.objects.create('They', *['they', 'them', 'their', 'theirs', 'themselves'])
        >>> xe_series = PronounSeries('Xe', *['Xe', 'Xer', 'Xis', 'Xis', 'Xerself'])
        >>> androgynous = Gender.objects.create('Androgynous')
        >>> androgynous.pronoun_series.add(1, 2)
        >>> androgynous.pronouns == {'they', 'them', 'theirs', 'xe', 'xer', 'xis'}
        True
        """

        all_pronouns = set()
        for series in list(self.pronoun_series.all()):
            all_pronouns |= series.all_pronouns

        return all_pronouns

    @property
    def subj(self):
        """
        :return: set of all subject pronouns used to describe the gender
        >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> masc_pronouns = PronounSeries('Masc', {'he', 'him', 'his'}, subj='he', obj='him')
        >>> bigender = Gender('Bigender', [fem_pronouns, masc_pronouns])
        >>> bigender.subj == {'he', 'she'}
        True
        """

        subject_pronouns = set()
        for series in list(self.pronoun_series.all()):
            subject_pronouns.add(series.subj)

        return subject_pronouns

    @property
    def obj(self):
        """
        :return: set of all object pronouns used to describe the gender
        >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> masc_pronouns = PronounSeries('Masc', {'he', 'him', 'his'}, subj='he', obj='him')
        >>> bigender = Gender('Bigender', [fem_pronouns, masc_pronouns])
        >>> bigender.obj == {'him', 'her'}
        True
        """

        subject_pronouns = set()
        for series in list(self.pronoun_series.all()):
            subject_pronouns.add(series.obj)
        return subject_pronouns


class Document(models.Model):
    """
    This model will hold the full text and
    metadata (author, title, publication date, etc.) of a document
    """
    author = models.CharField(max_length=255, blank=True)
    year = models.IntegerField(null=True, blank=True)
    new_attributes = models.JSONField(null=True, blank=True, default=dict)
    text = models.TextField(blank=True)
    title = models.CharField(max_length=255, blank=True)
    word_count = models.PositiveIntegerField(blank=True, null=True, default=None)
    tokenized_text = models.JSONField(null=True, blank=True, default=None)
    word_count_counter = models.JSONField(null=True, blank=True, default=dict)
    part_of_speech_tags = models.JSONField(null=True, blank=True, default=list)

    objects = DocumentManager()

    def _clean_quotes(self):
        """
        Scans through the text and replaces all of the smart quotes and apostrophes with their
        "normal" ASCII variants

        :param self: The Document to reformat
        :return: A string that is identical to `text`, except with its smart quotes exchanged
        """
        self.text = re.sub(r'[\“\”]', '\"', re.sub(r'[\‘\’]', '\'', self.text))
        self.save()
        return self.text

    def get_tokenized_text_wc_and_pos(self):
        """
        Tokenizes the text of a Document and returns it as a list of tokens, while removing all punctuation
        and converting everything to lowercase.

        :param self: The Document to tokenize
        :return: none
        """
        self._clean_quotes()
        tokens = nltk.word_tokenize(self.text)
        excluded_characters = set(string.punctuation)
        tokenized_text = [word.lower() for word in tokens if word not in excluded_characters]
        self.tokenized_text = tokenized_text
        self.word_count = len(self.tokenized_text)
        self.word_count_counter = Counter(self.tokenized_text)
        self.part_of_speech_tags = nltk.pos_tag(self.tokenized_text)
        self.save()

    def get_count_of_word(self, word):
        """
        Returns the number of instances of a word in the text.

        Note: This method is not case sensitive

        :param word: word to be counted in text
        :return: Number of occurrences of the word, as an int
        """
        try:
            return self.word_count_counter[word.lower()]
        except KeyError:
            return 0

    def get_count_of_words(self, words):
        """
        A helper method for retrieving the number of occurrences of a given set of words within
        a Document.

        Note: The method is not case sensitive.

        :param words: a list of strings.
        :return: a Counter with each word in words keyed to its number of occurrences.
        """
        return Counter({word: self.get_count_of_word(word) for word in words})

    def find_quoted_text(self):
        """
        Finds all of the quoted statements in the document text.

        :return: List of strings enclosed in double-quotations
        """
        text_list = self.text.split()
        quotes = []
        current_quote = []
        quote_in_progress = False
        quote_is_paused = False

        for word in text_list:
            if word[0] == "\"":
                quote_in_progress = True
                quote_is_paused = False
                current_quote.append(word)
            elif quote_in_progress:
                if not quote_is_paused:
                    current_quote.append(word)
                if word[-1] == "\"":
                    if word[-2] != ',':
                        quote_in_progress = False
                        quote_is_paused = False
                        quotes.append(' '.join(current_quote))
                        current_quote = []
                    else:
                        quote_is_paused = True
        return quotes

    def words_associated(self, target_word):
        """
        Returns a Counter of the words found after a given word.

        In the case of double/repeated words, the counter would include the word itself and the next
        new word.

        Note: the method is not case sensitive and words always return lowercase.

        :param target_word: Single word to search for in the document's text
        :return: a Python Counter() object with {associated_word: occurrences}
        """
        target_word = target_word.lower()
        word_count = Counter()
        check = False
        text = self.tokenized_text

        for word in text:
            if check:
                word_count[word] += 1
                check = False
            if word == target_word:
                check = True
        return word_count

    def get_word_windows(self, search_terms, window_size=2):
        """
        Finds all instances of `word` and returns a counter of the words around it.
        window_size is the number of words before and after to return, so the total window is
        2*window_size + 1.

        This is not case sensitive.

        :param search_terms: String or list of strings to search for
        :param window_size: integer representing number of words to search for in either direction
        :return: Python Counter object
        """

        if isinstance(search_terms, str):
            search_terms = [search_terms]

        search_terms = set(i.lower() for i in search_terms)

        counter = Counter()

        for text_window in windowed(self.tokenized_text, 2 * window_size + 1):
            if text_window[window_size] in search_terms:
                for surrounding_word in text_window:
                    if surrounding_word not in search_terms:
                        counter[surrounding_word] += 1

        return counter

    def get_word_freq(self, word):
        """
        Returns the frequency of appearance of a word in the document

        :param word: str to search for in document
        :return: float representing the portion of words in the text that are the parameter word
        """
        word_frequency = self.get_count_of_word(word) / self.word_count
        return word_frequency

    def get_word_freqs(self, words):
        """
        A helper method for retrieving the frequencies of a given set of words within a Document.

        :param words: a list of strings.
        :return: a dictionary of words keyed to float frequencies.
        """
        word_frequencies = {word: self.get_count_of_word(word) / self.word_count for word in words}
        return word_frequencies

    def get_part_of_speech_words(self, words, remove_swords=True):
        """
        A helper method for retrieving the number of occurrences of input words keyed to their
        NLTK tag values (i.e., 'NN' for noun).

        :param words: a list of strings.
        :param remove_swords: optional boolean, remove stop words from return.
        :return: a dictionary keying NLTK tag strings to Counter instances.
        """
        stop_words = set(nltk.corpus.stopwords.words('english'))
        document_pos_tags = self.part_of_speech_tags
        words_set = {word.lower() for word in words}
        output = {}

        for token, tag in document_pos_tags:
            lowered_token = token.lower()
            if remove_swords is True and token in stop_words:
                continue
            if token not in words_set:
                continue
            if tag not in output:
                output[tag] = Counter()
            output[tag][lowered_token] += 1

        return output

    def update_metadata(self, new_metadata):
        """
        Updates the metadata of the document without requiring a complete reloading
        of the text and other properties.

        :param new_metadata: dict of new metadata to apply to the document
        :return: None
        """
        default_fields = [field.name for field in self._meta.get_fields()]
        for key in new_metadata:
            if key not in default_fields:
                self.new_attributes[key] = new_metadata[key]
            else:
                setattr(self, key, new_metadata[key])

        if 'text' in new_metadata:
            self.text = new_metadata['text']
            self.get_tokenized_text_wc_and_pos()
        self.save()


class Corpus(models.Model):
    """
    This model will hold associations to other Documents and their
    metadata (author, title, publication date, etc.)
    """
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500, blank=True)
    documents = models.ManyToManyField(Document)

    class Meta:
        verbose_name_plural = "Corpora"

    def __str__(self):
        """Returns the title of the corpus"""
        return self.title

    def __len__(self):
        """Returns the number of documents associated with this corpus"""
        return len(self.document_set.all())

    def __iter__(self):
        """Yields each document associated with the corpus"""
        for this_document in self.document_set.all():
            yield this_document

    def __eq__(self, other):
        """Returns true if both of the corpora are associated with the same documents"""
        if not isinstance(other, Corpus):
            raise NotImplementedError("Only a Corpus can be compared to another Corpus.")

        if len(self) != len(other):
            return False

        if set(self.document_set.all()) == set(other.document_set.all()):
            return True
        else:
            return False


class NewResults(models.Model):
    """
    This model will persist the results from various proximity analysis functions.
    """

    results = models.JSONField()
    by_date = models.JSONField()
    by_document = models.JSONField()
    by_gender = models.JSONField()
    by_metadata = models.JSONField()
    by_overlap = models.JSONField()

