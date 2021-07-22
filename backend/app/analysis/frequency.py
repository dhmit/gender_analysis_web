from collections import Counter


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
        count[gender.label] = doc_obj.get_count_of_words(gender.pronouns)
        frequency[gender.label] = doc_obj.get_word_freqs(gender.pronouns)
    relative = _get_gender_word_frequencies_relative(count)

    output = {
        'count': count,
        'frequency': frequency,
        'relative': relative
    }

    return output
