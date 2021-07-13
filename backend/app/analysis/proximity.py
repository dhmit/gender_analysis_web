import nltk
from collections import Counter
from more_itertools import windowed

from ..models import (
    Document,
    Gender,
    Corpus,
)


def run_analysis(corpus_id, gender_ids, word_window):
    """
    Generates a dictionary of dictionaries for each `Document` object. Each dictionary maps a `Gender` to a word count
    of words within a specified window of that `Gender`'s pronouns.

    :param corpus_id: An int representing a `Corpus` instance
    :param gender_ids: A list of ints representing `Gender` ids
    :param word_window: An integer describing the number of words to look at of each side of a gendered word

    :return: A dict mapping `Document` ids to a dict mapping strings (`Gender` labels) to a `Counter` instance.
    """
    results = {}

    doc_ids = Corpus.objects.filter(pk=corpus_id).values_list('documents__pk', flat=True)

    for key in doc_ids:
        results[key] = _generate_gender_token_counters(
            Document.objects.values_list('tokenized_text', flat=True).filter(pk=key),
            gender_ids,
            word_window
        )

    return results


def _generate_gender_token_counters(text_query, gender_ids, word_window):
    """
    Generates a dictionary mapping `Gender`s to a word count of words within a specified window of the `Gender`'s
    pronouns.

    :param text_query: An unevaluated, length-1 `QuerySet` that returns a list of strings when evaluated
    :param gender_ids: A list of ints representing `Gender` ids
    :param word_window: An integer describing the number of words to look at of each side of a gendered word

    :return: A dict mapping strings (`Gender` labels) to a `Counter` instance.

    """

    results = {}

    for gender_id in gender_ids:
        gender = Gender.objects.get(pk=gender_id)

        doc_result = _generate_token_counter(text_query, gender, word_window)
        results[gender.label] = doc_result

    return results


def _generate_token_counter(text_query, gender, word_window):
    # pylint: disable=too-many-locals
    """
    Generates a 'Counter' instance mapping words to their frequency within a text.

    :param text_query: An unevaluated, length-1 `QuerySet` that returns a list of strings when evaluated
    :param gender: A `Gender` object
    :param word_window: an integer describing the number of words to look at of each side of a gendered word

    :return: A 'Counter' instance showcasing the numbered occurrences of words around a gendered pronoun

    """

    output = Counter()

    for words in windowed(text_query.get(), 2 * word_window + 1):
        if words[word_window].lower() in gender.pronouns:
            words = list(words)

            for index, word in enumerate(words):
                words[index] = word.lower()

            tagged_tokens = nltk.pos_tag(words)
            for tag_index, _ in enumerate(tagged_tokens):
                word = words[tag_index]
                output[word] += 1

    return output
