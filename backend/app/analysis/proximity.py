import nltk
from collections import Counter
from more_itertools import windowed

from ..models import (
    Document,
    Gender,
)


def run_analysis(doc_ids, gender_ids, tags, word_window):
    """
    Generates a dictionary of dictionaries for each `Document` object. Each dictionary maps a `Gender` to a word count
    of words within a specified window of that `Gender`'s pronouns.

    :param doc_ids: A list of ints representing `Document` ids
    :param gender_ids: A list of ints representing `Gender` ids
    :param tags: A Python dictionary mapping parts of speech tags to their definitions
    :param word_window: An integer describing the number of words to look at of each side of a gendered word

    :return: A dict mapping `Document` ids to a dict mapping strings (`Gender` labels) to a `Counter` instance.
    """
    results = {}

    for key in doc_ids:
        results[key] = generate_gender_token_counters(
            Document.objects.values_list('tokenized_text', flat=True).filter(pk=key),
            gender_ids,
            tags,
            word_window
        )

    return results


def generate_gender_token_counters(text_query, gender_ids, tags, word_window):
    """
    Generates a dictionary mapping `Gender`s to a word count of words within a specified window of the `Gender`'s
    pronouns.

    :param text_query: An unevaluated, length-1 `QuerySet` that returns a list of strings when evaluated
    :param gender_ids: A list of ints representing `Gender` ids
    :param tags: A Python dictionary mapping parts of speech tags to their definitions
    :param word_window: An integer describing the number of words to look at of each side of a gendered word

    :return: A dict mapping strings (`Gender` labels) to a `Counter` instance.

    """

    results = {}

    for gender_id in gender_ids:
        doc_result = generate_token_counter(text_query, gender_id, tags, word_window)
        results.update({Gender.objects.values_list('label', flat=True).get(pk=gender_id): doc_result})

    return results


def generate_token_counter(text_query, gender_id, tags, word_window):
    # pylint: disable=too-many-locals
    """
    Generates a 'Counter' instance mapping words to their frequency within a text.

    :param text_query: An unevaluated, length-1 `QuerySet` that returns a list of strings when evaluated
    :param gender_id: An int representing a the id of some `Gender` object in the database
    :param tags: a Python dictionary mapping parts of speech tags to their definitions
    :param word_window: an integer describing the number of words to look at of each side of a gendered word

    :return: A 'Counter' instance showcasing the numbered occurrences of words around a gendered pronoun

    """

    output = Counter()

    gender = Gender.objects.get(pk=gender_id)

    for words in windowed(text_query.get(), 2 * word_window + 1):
        if words[word_window].lower() in gender.pronouns:
            words = list(words)

            for index, word in enumerate(words):
                words[index] = word.lower()

            tagged_tokens = nltk.pos_tag(words)
            for tag_index, _ in enumerate(tagged_tokens):
                if tagged_tokens[tag_index][1] in tags:
                    word = words[tag_index]
                    output[word] += 1

    return output
