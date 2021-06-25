from collections import Counter
from typing import Dict, Optional, Sequence, Tuple, Union
from app.models import Gender

GenderCounts = Dict[Gender, Counter]

def _get_gender_word_frequencies_relative(gender_word_counts: GenderCounts):

    output = {}
    total_word_count = 0
    for gender in gender_word_counts:
        for word in gender_word_counts[gender]:
            total_word_count += gender_word_counts[gender][word]

    for gender in gender_word_counts:
        output[gender] = {}
        for word, original_count in gender_word_counts[gender].items():
            try:
                frequency = original_count / total_word_count
            except ZeroDivisionError:
                frequency = 0
            output[gender][word] = frequency

    return output

def _run_frequency_analysis(texts, genders):
    """
    :param document: a list of strings presenting the documents
    :param pronouns: a list of strings presenting the pronouns
    """
    count = {}
    frequencies = {}
    relatives = {}

    for document in texts:
        count[document] = Counter()
        frequencies[document] = {}
        relatives[document] = {}
        for gender in genders:
            count[document][gender] = document.get_count_of_words(gender.identifiers)
            frequencies[document][gender] = document.get_word_frequencies(gender.identifiers)
        relatives[document] = _get_gender_word_frequencies_relative(count[document])

    return count, frequencies, relatives