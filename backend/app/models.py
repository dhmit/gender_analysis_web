"""
Models for the gender analysis web app.
"""
import nltk
import string
from collections import Counter
from more_itertools import windowed
from django.db import models
from .fields import LowercaseCharField


class Pronoun(models.Model):
    """
    A model that allows users to define an individual pronoun and its type
    (e.g. subject, object, reflexive, etc). Pronouns are case-insensitive and will be
    converted to lowercase.
    """
    PRONOUN_TYPES = [
        ('subj', 'Subject'),
        ('obj', 'Object'),
        ('pos_det', 'Possessive determiner'),
        ('pos_pro', 'Possessive pronoun'),
        ('reflex', 'Reflexive'),
    ]

    identifier = LowercaseCharField(max_length=40)
    type = models.CharField(max_length=7, choices=PRONOUN_TYPES)

    def __repr__(self):
        return f'Pronoun({self.identifier, self.type})'

    def __str__(self):
        return f'Pronoun: {self.identifier}\nType: {self.get_type_display()}'

    def __eq__(self, other):
        return self.identifier == other.identifier


class DocumentManager(models.Manager):
    def create_document(self, attributes):
        doc = self.create(attributes)
        doc.get_tokenized_text()
        doc.get_word_count()
        doc.get_word_count_counter()
        doc.get_part_of_speech_tags()
        return doc


class Document(models.Model):
    """
    This model will hold the full text and
    metadata (author, title, publication date, etc.) of a document
    """
    author = models.CharField(max_length=255, blank=True)
    date = models.IntegerField(null=True, blank=True)
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

        # Define the quotes that will be swapped out
        smart_quotes = {
            '“': '"',
            '”': '"',
            "‘": "'",
            "’": "'",
        }

        # Replace all entries one by one
        output_text = self.text
        for quote in smart_quotes:
            output_text = output_text.replace(quote, smart_quotes[quote])
        self.text = output_text
        self.save()
        return self.text

    def get_tokenized_text(self):
        """
        Tokenizes the text of a Document and returns it as a list of tokens, while removing all punctuation
        and converting everything to lowercase.

        :param self: The Document to tokenize
        :return: List of each word in the Document
        """

        # Excluded characters: !"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
        if self.tokenized_text is None:
            self._clean_quotes()
            tokens = nltk.word_tokenize(self.text)
            excluded_characters = set(string.punctuation)
            tokenized_text = [word.lower() for word in tokens if word not in excluded_characters]
            self.tokenized_text = tokenized_text
            self.save()
        return self.tokenized_text

    def get_count_of_word(self, word):
        """
        Returns the number of instances of a word in the text.

        If this is your first time running this method, this can be slow.

        :param word: word to be counted in text
        :return: Number of occurrences of the word, as an int
        """

        # If word_counts were not previously initialized, do it now and store it for the future.
        self.get_word_count_counter()
        return self.word_count_counter[word.lower()]

    def get_count_of_words(self, words):
        """
        A helper method for retrieving the number of occurrences of a given set of words within
        a Document.

        :param words: a list of strings.
        :return: a Counter with each word in words keyed to its number of occurrences.
        """
        return Counter({word: self.get_count_of_word(word) for word in words})

    def get_word_count(self):
        """
        Lazy-loading for **Document.word_count** attribute.
        Returns the number of words in the document.
        The word_count attribute is useful for the get_word_freq function.
        However, it is performance-wise costly, so it's only loaded when it's actually required.

        :param self: The Document to get the word count of
        :return: Number of words in the document's text as an int

        """
        if self.word_count is None:
            self.word_count = len(self.get_tokenized_text())
            self.save()
        return self.word_count

    def get_word_count_counter(self):
        """
        Returns a counter object of all of the words in the text.

        If this is your first time running this method, this can be slow.

        :return: Python Counter object
        """

        # If word_counts were not previously initialized, do it now and store it for the future.
        if not self.word_counts_counter:
            self.word_counts_counter = Counter(self.get_tokenized_text())
        return self.word_counts_counter

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
        .. _words-associated:

        Returns a Counter of the words found after a given word.

        In the case of double/repeated words, the counter would include the word itself and the next
        new word.

        Note: words always return lowercase.

        :param target_word: Single word to search for in the document's text
        :return: a Python Counter() object with {associated_word: occurrences}
        """
        target_word = target_word.lower()
        word_count = Counter()
        check = False
        text = self.get_tokenized_text()

        for word in text:
            if check:
                word_count[word] += 1
                check = False
            if word == target_word:
                check = True
        return word_count

    # pylint: disable=line-too-long
    def get_word_windows(self, search_terms, window_size=2):
        """
        .. _get-word-windows:

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

        for text_window in windowed(self.get_tokenized_text(), 2 * window_size + 1):
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

        word_frequency = self.get_count_of_word(word) / self.get_word_count()
        return word_frequency

    def get_word_freqs(self, words):
        """
        A helper method for retrieving the frequencies of a given set of words within a Document.

        :param words: a list of strings.
        :return: a dictionary of words keyed to float frequencies.
        """
        word_frequencies = {word: self.get_count_of_word(word) / self.get_word_count() for word in words}

        return word_frequencies

    def get_part_of_speech_tags(self):
        """
        .. _get-pos:

        Returns the part of speech tags as a list of tuples. The first part of each tuple is the
        term, the second one the part of speech tag.

        Note: the same word can have a different part of speech tags.

        :return: List of tuples (term, speech_tag)
        """

        if not self.part_of_speech_tags:
            text = nltk.word_tokenize(self.text)
            pos_tags = nltk.pos_tag(text)

            self.part_of_speech_tags = pos_tags
            self.save()
        return self.part_of_speech_tags

    def get_part_of_speech_words(self, words, remove_swords=True):
        """
        A helper method for retrieving the number of occurrences of input words keyed to their
        NLTK tag values (i.e., 'NN' for noun).

        :param words: a list of strings.
        :param remove_swords: optional boolean, remove stop words from return.
        :return: a dictionary keying NLTK tag strings to Counter instances.
        """
        stop_words = set(nltk.corpus.stopwords.words('english'))
        document_pos_tags = self.get_part_of_speech_tags()
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

        'filename' cannot be updated with this method.

        :param new_metadata: dict of new metadata to apply to the document
        :return: None
        """
        default_fields = [field.name for field in self._meta.get_fields()]
        if not isinstance(new_metadata, dict):
            raise ValueError(
                f'new_metadata must be a dictionary of metadata keys, not type {type(new_metadata)}'
            )

        for key in new_metadata:
            if key == 'date':
                try:
                    new_metadata[key] = int(new_metadata[key])
                except ValueError as err:
                    raise ValueError(
                        f"the metadata field 'date' must be a number for the document,"
                        f" not '{new_metadata['date']}'"
                    ) from err
            if key not in default_fields:
                self.new_attributes[key] = new_metadata[key]
            else:
                setattr(self, key, new_metadata[key])

        if 'text' in new_metadata:
            self.text = self._clean_quotes()
            self.word_count = None
            self.tokenized_text = None
            self.word_counts_counter = dict()
            self.part_of_speech_tags = list()
            self.get_tokenized_text()
            self.get_word_count()
            self.get_word_count_counter()
            self.get_part_of_speech_tags()

        self.save()
