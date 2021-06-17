import re
import string
from collections import Counter

import nltk


def word_count(document_obj):
    """
    Lazy-loading for **Document.word_count** attribute.
    Returns the number of words in the document.
    The word_count attribute is useful for the get_word_freq function.
    However, it is performance-wise costly, so it's only loaded when it's actually required.

    :return: Number of words in the document's text as an int

    """
    if document_obj.word_count is None:
        document_obj.word_count = len(get_tokenized_text(document_obj))
        document_obj.save()
    return document_obj.word_count


def _clean_quotes(text):
    """
    Scans through the text and replaces all of the smart quotes and apostrophes with their
    "normal" ASCII variants

    >>> smart_text = 'This is a “smart” phrase'
    >>> _clean_quotes(smart_text)
    'This is a "smart" phrase'

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
    output_text = text
    for quote in smart_quotes:
        output_text = output_text.replace(quote, smart_quotes[quote])

    return output_text


def get_tokenized_text(document_obj):
    """
    Tokenizes the text and returns it as a list of tokens, while removing all punctuation.

    Note: This does not currently properly handle dashes or contractions.

    :return: List of each word in the Document
    """

    # Excluded characters: !"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
    if document_obj.tokenized_text is None:
        tokens = nltk.word_tokenize(document_obj.text)
        excluded_characters = set(string.punctuation)
        tokenized_text = [word.lower() for word in tokens if word not in excluded_characters]
        document_obj.tokenized_text = tokenized_text
        document_obj.save()
        return tokenized_text

    else:
        return document_obj.tokenized_text

def get_wordcount_counter(document_obj):
    """
    Returns a counter object of all of the words in the text.

    If this is your first time running this method, this can be slow.

    :return: Python Counter object
    """

    # If word_counts were not previously initialized, do it now and store it for the future.
    if not document_obj._word_counts_counter:
        document_obj._word_counts_counter = Counter(get_tokenized_text(document_obj))
    return document_obj._word_counts_counter