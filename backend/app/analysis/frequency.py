from collections import Counter
from typing import Dict, Optional, Sequence, Tuple, Union
from app.models import (
    Gender,
)

GenderCounts = Dict[Gender, Counter]
GenderFrequencies = Dict[Gender, WordFrequency]

def _get_gender_word_frequencies_relative(gender_word_counts: GenderCounts) -> GenderFrequencies:
    """
    A private helper function that examines identifier counts keyed to Gender instances,
    determines the total count value of all identifiers across Gender instances,
    and returns the percentage of each identifier count over the total count.

    :param gender_word_counts: a dictionary keying gender instances to string identifiers keyed to
                               integer counts.
    :return: a dictionary with the integer counts transformed into float values representing
             the identifier count as a percentage of the total identifier counts across all
             identifiers.
    """

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

def _run_analysis(texts, genders):
    """
    A private helper method for running the primary analysis of GenderFrequencyAnalyzer.
    This method generates three dictionaries: one (count) keying Document instances
    to Gender instances to Counter instances representing the total number of instances
    of each Gender's identifiers in a given Document; one (frequency) keying Document instances
    to Gender instances to dictionaries of the shape {str:float} representing the total number
    of instances of each Gender's identifiers over the total word count of that Document; and
    one (relative) keying Document instances to Gender instances to dicationaries of the shape
    {str:float} representing the relative percentage of Gender identifiers across all Gender
    instances in a given Document instance.

    :param texts: a list of strings presenting the documents
    :param genders: a list of strings presenting the pronouns
    :return: :return: a tuple containing three dictionaries
    """
    count = {}
    frequencies = {}
    relatives = {}

    for document in texts:
        count[document] = Counter()
        frequencies[document] = {}
        relatives[document] = {}
        for gender in genders:
            count[document][gender] = document.get_count_of_words(gender.pronouns)
            frequencies[document][gender] = document.get_word_freqs(gender.pronouns)
        relatives[document] = _get_gender_word_frequencies_relative(count[document])

    return count, frequencies, relatives