import nltk
from collections import Counter
from more_itertools import windowed

from ..models import (
    Document,
    Gender,
    Corpus,
)


def run_analysis(corpus_id, word_window):
    """
    Generates a dictionary of dictionaries for each `Document` object. Each dictionary maps a `Gender` to a word count
    of words within a specified window of that `Gender`'s pronouns.

    :param corpus_id: An int representing a `Corpus` instance
    :param word_window: An integer describing the number of words to look at of each side of a gendered word

    :return: A dict mapping `Document` ids to a dict mapping strings (`Gender` labels) to a `Counter` instance.
    """
    results = {}
    genders = set(Gender.objects.all())

    doc_ids = Corpus.objects.filter(pk=corpus_id).values_list('documents__pk', flat=True)

    for key in doc_ids:
        results[key] = generate_gender_token_counters(
            Document.objects.values_list('part_of_speech_tags', flat=True).filter(pk=key).get(),
            genders,
            word_window
        )

    return results


def generate_gender_token_counters(pos_tags, genders, word_window):
    """
    Generates a dictionary mapping `Gender`s to a word count of words within a specified window of the `Gender`'s
    pronouns.

    :param pos_tags: A list of 2-element tuples: the first element is a word (str), and the second element is a
        part-of-speech tag (str).
    :param genders: A set of Gender objects
    :param word_window: An integer describing the number of words to look at of each side of a gendered word

    :return: A dict mapping strings (`Gender` labels) to a `Counter` instance.

    """

    results = {}

    for gender in genders:
        doc_result = generate_token_counter(pos_tags, gender, word_window)
        results[gender.label] = doc_result

    return results


def generate_token_counter(pos_tags, gender, word_window):
    # pylint: disable=too-many-locals
    """
    Generates a 'Counter' instance mapping words to their frequency within a text.

    :param pos_tags: A list of 2-element tuples: the first element is a word (str), and the second element is a
        part-of-speech tag (str).
    :param gender: A `Gender` object
    :param word_window: An integer describing the number of words to look at on each side of a gendered word

    :return: A 'Dict' instance mapping the part of speech tag to a 'Counter' instance,
        which features the numbered occurrences of words around a gendered pronoun

    """

    output = {}

    for tagged_tokens in windowed(pos_tags, 2 * word_window + 1):
        if tagged_tokens[word_window][0].lower() in gender.pronouns:

            for index, tagged_token in enumerate(tagged_tokens):
                word = tagged_token[0].lower()
                pos_tag = tagged_token[1]

                output.setdefault(pos_tag, Counter())
                output[pos_tag][word] += 1

    return output
