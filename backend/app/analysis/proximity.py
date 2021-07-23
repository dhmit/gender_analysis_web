from collections import Counter
from itertools import chain
from more_itertools import windowed

from ..models import (
    Document,
    Gender,
    Corpus,
    PronounSeries,
)


def run_analysis(corpus_id, word_window):
    """
    Generates a dictionary of dictionaries for each `Document` object. Each dictionary maps a `Gender` to a word count
    of words within a specified window of that `Gender`'s pronouns.

    :param corpus_id: An int representing a `Corpus` instance
    :param word_window: An integer describing the number of words to look at of each side of a gendered word

    :return: A dict mapping `Document` ids to a dict mapping strings (`Gender` labels) to a `Counter` instance.
        The dict is of the following form: {int: {Gender: {str: {str, Counter(str, int)}}}}
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

    :return: A dict mapping a `Gender` instance to a dict mapping a 'PRONOUN_TYPE' to a dict instance
     mapping part of speech tag to a `Counter` instance.

    """

    results = {}

    for gender in genders:
        results[str(gender)] = dict()

        for PRONOUN_TYPE in PronounSeries.PRONOUN_TYPES:
            pronoun_set = gender.pronoun_series.values_list(PRONOUN_TYPE, flat=True)
            doc_result = generate_token_counter(pos_tags, pronoun_set, word_window)
            results[str(gender)][PRONOUN_TYPE] = doc_result

    return results


def generate_token_counter(pos_tags, pronoun_set, word_window):
    # pylint: disable=too-many-locals
    """
    Generates a 'Counter' instance mapping words to their frequency within a text.

    :param pos_tags: A list of 2-element tuples: the first element is a word (str), and the second element is a
        part-of-speech tag (str).
    :param pronoun_set: A QuerySet that returns a set of strings (pronouns) when evaluated, filtered by the type of
        pronoun
    :param word_window: An integer describing the number of words to look at on each side of a gendered word

    :return: A 'Dict' instance mapping the part of speech tag to a 'Counter' instance,
        which features the numbered occurrences of words around a gendered pronoun.

    """
    output = {}
    padding = [None] * word_window

    for tagged_tokens in windowed(chain(padding, pos_tags, padding), 2 * word_window + 1):
        candidate = tagged_tokens[word_window][0].lower()

        if candidate in pronoun_set:

            for index, tagged_token in enumerate(tagged_tokens):
                if tagged_token is not None:

                    word = tagged_token[0].lower()
                    if word != candidate:

                        pos_tag = tagged_token[1]
                        output.setdefault(pos_tag, Counter())
                        output[pos_tag][word] += 1

    return output
