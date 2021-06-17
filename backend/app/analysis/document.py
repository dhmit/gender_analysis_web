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