from collections import Counter
from ..models import (
    Corpus,
    Document,
    Gender
)


def _get_gender_word_frequencies_relative(gender_word_counts):
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


def run_single_analysis(doc_obj, genders):
    """
    This method generates a dictionary that includes a Counter (count) that keys
    Document instances to Gender instances to Counter instances representing the total
    number of instances of each Gender's pronouns in a given Document, a dictionary (frequency)
    keying Document instances to Gender instances to dictionaries of the shape {str:float}
    representing the total number of instances of each Gender's pronouns over the total word count
    of that Document; and a dictionary (relative) keying Document instances to Gender instances
    to dictionaries of the shape {str:float} representing the relative percentage of Gender
    pronouns across all Gender instances in a given Document instance.

    :param doc_obj: an instance of the Document model
    :param genders: a list of Gender objects
    :return: a dictionary containing the frequency analyses of the Document instance
    """
    count = Counter()
    frequency = {}

    for gender in genders:
        count[gender] = doc_obj.get_count_of_words(gender.pronouns)
        frequency[gender] = doc_obj.get_word_freqs(gender.pronouns)
    relative = _get_gender_word_frequencies_relative(count)

    output = {
        'count': count,
        'frequency': frequency,
        'relative': relative
    }

    return output


def run_analysis(corpus_id, gender_ids):
    """
        This method generates a dictionary of dictionaries for each Document instance in the Corpus.
        Each dictionary maps the type of frequency analysis (count, frequency, relative) to the
        analysis itself.

        :param corpus_id: the ID of a Corpus instance
        :param gender_ids: a list of integers representing Gender primary keys
        :return: a dictionary mapping the Document IDs to the frequency analyses of the Document instance
    """
    results = {}
    genders = Gender.objects.filter(id__in=gender_ids)
    doc_ids = Corpus.objects.filter(pk=corpus_id).values_list('documents__pk', flat=True)
    for pk in doc_ids:
        results[pk] = run_single_analysis(Document.objects.get(id=pk), genders)
    return results
