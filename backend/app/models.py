"""
Models for the ***** app.
"""
from django.db import models
import nltk
import string
from collections import Counter

# no models yet -- write me!

class Document(models.Model):
    """
    This model will hold the full text and
    metadata (author, title, publication date, etc.) of a document
    """
    author = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    date = models.IntegerField(null=True, blank=True)
    text = models.TextField(blank=True)
    label = models.CharField(max_length=255, blank=True)
    word_count = models.PositiveIntegerField(blank=True, null=True, default=None)
    tokenized_text = models.JSONField(null=True, blank=True, default=None)
    _word_counts_counter = models.JSONField(null=True, blank=True, default=dict)
    _part_of_speech_tags = models.JSONField(null=True, blank=True, default=list)

    def _clean_quotes(self):
        """
        Scans through the text and replaces all of the smart quotes and apostrophes with their
        "normal" ASCII variants

        :param text: The string to reformat
        :return: A string that is idential to `text`, except with its smart quotes exchanged
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
        Tokenizes the text and returns it as a list of tokens, while removing all punctuation.

        Note: This does not currently properly handle dashes or contractions.

        :return: List of each word in the Document
        """

        # Excluded characters: !"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
        if self.tokenized_text is None:
            tokens = nltk.word_tokenize(self.text)
            excluded_characters = set(string.punctuation)
            tokenized_text = [word.lower() for word in tokens if word not in excluded_characters]
            self.tokenized_text = tokenized_text
            self.save()
        return self.tokenized_text

    def get_word_count(self):
        """
        Lazy-loading for **Document.word_count** attribute.
        Returns the number of words in the document.
        The word_count attribute is useful for the get_word_freq function.
        However, it is performance-wise costly, so it's only loaded when it's actually required.

        :return: Number of words in the document's text as an int

        """
        if self.word_count is None:
            self.word_count = len(self.get_tokenized_text())
            self.save()
        return self.word_count

    def get_wordcount_counter(self):
        """
        Returns a counter object of all of the words in the text.

        If this is your first time running this method, this can be slow.

        :return: Python Counter object
        """

        # If word_counts were not previously initialized, do it now and store it for the future.
        if not self._word_counts_counter:
            self._word_counts_counter = Counter(self.get_tokenized_text())
        return self._word_counts_counter