import re
import string
from collections import Counter
from pathlib import Path

from gutenberg_cleaner import simple_cleaner
from more_itertools import windowed
import nltk

def word_count(document_obj):
    """
    Lazy-loading for **Document.word_count** attribute.
    Returns the number of words in the document.
    The word_count attribute is useful for the get_word_freq function.
    However, it is performance-wise costly, so it's only loaded when it's actually required.

    :return: Number of words in the document's text as an int

    >>> from gender_analysis import Document
    >>> from pathlib import Path
    >>> from gender_analysis.testing.common import TEST_DATA_DIR
    >>> document_metadata = {'author': 'Austen, Jane', 'title': 'Persuasion', 'date': '1818',
    ...                      'filename': 'austen_persuasion.txt',
    ...                      'filepath': Path(TEST_DATA_DIR, 'sample_novels',
    ...                                       'texts', 'austen_persuasion.txt')}
    >>> austen = Document(document_metadata)
    >>> austen.word_count
    83285

    """
    if document_obj._word_count is None:
        document_obj._word_count = len(document_obj.get_tokenized_text())
    return document_obj._word_count


def _clean_quotes(text):
    """
    Scans through the text and replaces all of the smart quotes and apostrophes with their
    "normal" ASCII variants

    >>> from gender_analysis import Document
    >>> smart_text = 'This is a “smart” phrase'
    >>> Document._clean_quotes(smart_text)
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

    >>> from gender_analysis import Document
    >>> from pathlib import Path
    >>> from gender_analysis.testing.common import TEST_DATA_DIR
    >>> document_metadata = {'author': 'Austen, Jane', 'title': 'Persuasion', 'date': '1818',
    ...                      'filename': 'test_text_1.txt',
    ...                      'filepath': Path(TEST_DATA_DIR,
    ...                                       'document_test_files', 'test_text_1.txt')}
    >>> austin = Document(document_metadata)
    >>> tokenized_text = austin.get_tokenized_text()
    >>> tokenized_text
    ['allkinds', 'of', 'punctuation', 'and', 'special', 'chars']

    """

    # Excluded characters: !"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
    if document_obj._tokenized_text is None:

        excluded_characters = set(string.punctuation)
        cleaned_text = ''
        for character in document_obj.text:
            if character not in excluded_characters:
                cleaned_text += character

        tokenized_text = cleaned_text.lower().split()
        document_obj._tokenized_text = tokenized_text
        return tokenized_text

    else:
        return document_obj._tokenized_text