import nltk
from collections import Counter
from more_itertools import windowed
from functools import reduce
from ..common import compute_bin_year, SWORDS_ENG

from ..models import (
    Document,
    Gender,
    Corpus,
    ProximityAnalyses,
)


def by_date(corpus_id,
            word_window,
            time_frame,
            bin_size,
            sort,
            diff,
            limit,
            remove_swords):
    """
    Return analysis organized by date.

    :param corpus_id: An int representing a `Corpus` instance
    :param word_window: An integer describing the number of words to look at of each side of a gendered word
    :param time_frame: a tuple of the format (start_date, end_date).
    :param bin_size: int for the number of years represented in each list of frequencies
    :param sort: Optional[bool], return Dict[int, Sequence[Tuple[str, int]]]
    :param diff: return the differences between genders.
    :param limit: Optional[int], if sort=True, return n=limit number of items in desc order.
    :param remove_swords: Optional[bool], remove stop words from return

    :return: a dictionary of the shape { str(Gender.label): { str(token): int } } or
             { str(Gender.label): [(str(token), int)] }
    """

    output = {}

    analysis_query = ProximityAnalyses.objects.filter(
        corpus__pk='corpus_id',
        word_window=word_window
    )

    if not analysis_query.filter(by_date=dict()).exists():
        # TENTATIVE! Debating whether or not to return the dictionary or the whole model to the view
        return analysis_query.values_list('by_date', flat=True).get()

    results_query = analysis_query.values_list(
        'results', flat=True
    )

    all_gender_labels = Gender.objects.values_list('label', flat=True)

    for bin_start_year in range(time_frame[0], time_frame[1], bin_size):
        output[bin_start_year] = {label: Counter() for label in all_gender_labels}

    doc_ids = Corpus.objects.filter(pk=corpus_id).values_list('documents__pk', flat=True)

    for each_id in doc_ids:
        doc_year = Document.objects.values_list('year', flat=True).filter(pk=each_id)
        bin_year = compute_bin_year(doc_year, time_frame[0], bin_size)

        if bin_year not in output:
            continue

        for gender_label in all_gender_labels:
            output[bin_year][gender_label] = merge_token_counters(
                [results_query.get()[each_id][gender_label], output[bin_year][gender_label]]
            )

    by_date_results = apply_result_filters(output,
                                           sort=sort,
                                           diff=diff,
                                           limit=limit,
                                           remove_swords=remove_swords)

    analysis = analysis_query.get()
    analysis.by_date = by_date_results
    analysis.save()

    # TENTATIVE! Debating whether or not to return the dictionary or the whole model to the view
    return by_date_results


def by_document(
        corpus_id,
        word_window,
        sort,
        diff,
        limit,
        remove_swords):
    """
    Return analysis organized by Document.

    :param corpus_id: An int representing a `Corpus` instance
    :param word_window: An integer describing the number of words to look at of each side of a gendered word
    :param sort: Optional[bool], return Dict[int, Sequence[Tuple[str, int]]]
    :param diff: return the differences between genders.
    :param limit: Optional[int], if sort=True, return n=limit number of items in desc order.
    :param remove_swords: Optional[bool], remove stop words from return

    :return: a dictionary of the shape { str(Gender.label): { str(token): int } } or
             { str(Gender.label): [(str(token), int)] }
    """

    output = {}

    analysis_query = ProximityAnalyses.objects.filter(
        corpus__pk='corpus_id',
        word_window=word_window
    )

    if not analysis_query.filter(by_document=dict()).exists():
        return analysis_query.values_list('by_document', flat=True).get()

    results_query = analysis_query.values_list(
        'results', flat=True
    )

    doc_ids = Corpus.objects.filter(pk=corpus_id).values_list('documents__pk', flat=True)

    for document_id in doc_ids:
        output[Document.objects.values_list('title', flat=True).filter(pk=document_id)] = results_query.get()[document_id]

    by_document_results = apply_result_filters(output,
                                               sort=sort,
                                               diff=diff,
                                               limit=limit,
                                               remove_swords=remove_swords)

    analysis = analysis_query.get()
    analysis.by_document = by_document_results
    analysis.save()

    # TENTATIVE! Debating whether or not to return the dictionary or the whole model to the view
    return by_document_results


def by_gender(
        corpus_id,
        word_window,
        sort,
        diff,
        limit,
        remove_swords):
    """
    Return analysis organized by Document. Merges all words across texts
    into dictionaries sorted by gender.

    :param corpus_id: An int representing a `Corpus` instance
    :param word_window: An integer describing the number of words to look at of each side of a gendered word
    :param sort: Optional[bool], return Dict[str, Sequence[Tuple[str, int]]]
    :param diff: return the differences between genders.
    :param limit: Optional[int], if sort=True, return n=limit number of items in desc order.
    :param remove_swords: Optional[bool], remove stop words from return

    :return: a dictionary of the shape {Gender.label: {str: int, ...}, ...}
    """

    merged_results = {}

    all_gender_labels = Gender.objects.values_list('label', flat=True)
    doc_ids = Corpus.objects.filter(pk=corpus_id).values_list('documents__pk', flat=True)

    analysis_query = ProximityAnalyses.objects.filter(
        corpus__pk='corpus_id',
        word_window=word_window
    )

    if not analysis_query.filter(by_gender=dict()).exists():
        return analysis_query.values_list('by_gender', flat=True).get()

    results_query = analysis_query.values_list(
        'results', flat=True
    )

    for gender_label in all_gender_labels:
        new_gender_token_counters = [
            results_query.get()[document_id][gender_label] for document_id in doc_ids
        ]
        merged_results[gender_label] = {}
        merged_results[gender_label] = merge_token_counters(new_gender_token_counters)

    output = merged_results

    if remove_swords:
        output = remove_swords(output)

    if diff:
        output = diff_gender_token_counters(output)

    if sort:
        output = sort_gender_token_counters(output, limit=limit)

    analysis = analysis_query.get()
    analysis.by_gender = output
    analysis.save()

    # TENTATIVE! Debating whether or not to return the dictionary or the whole model to the view
    return output

def by_metadata(
        corpus_id,
        word_window,
        metadata_field,
        sort,
        diff,
        limit,
        remove_swords):
    """
    Return analysis organized by Document metadata. Merges all words across texts
    into dictionaries sorted by provided metadata_key.

    :param corpus_id: An int representing a `Corpus` instance
    :param word_window: An integer describing the number of words to look at of each side of a gendered word
    :param metadata_field: a string.
    :param sort: Optional[bool], return Dict[str, Sequence[Tuple[str, int]]]
    :param diff: return the differences between genders.
    :param limit: Optional[int], if sort=True, return n=limit number of items in desc order.
    :param remove_swords: Optional[bool], remove stop words from return

    :return: a dictionary of the shape {Gender.label: {str: int , ...}, ...}.
    """

    output = {}

    analysis_query = ProximityAnalyses.objects.filter(
        corpus__pk='corpus_id',
        word_window=word_window
    )

    if not analysis_query.filter(by_metadata=dict()).exists():
        return analysis_query.values_list('by_metadata', flat=True).get()

    results_query = analysis_query.values_list(
        'results', flat=True
    )

    all_gender_labels = Gender.objects.values_list('label', flat=True)

    for document_id, gender_token_counters in results_query.get().items():
        matching_field = Document.objects.values_list(metadata_field, flat=True).filter(pk=document_id)

        if matching_field not in output:
            output[matching_field] = {}

        for gender_label in all_gender_labels:
            if gender_label not in output[matching_field]:
                output[matching_field][gender_label] = Counter()
            output[matching_field][gender_label] = merge_token_counters([
                gender_token_counters[gender_label],
                output[matching_field][gender_label]
            ])

    by_metadata_results = apply_result_filters(output,
                                               sort=sort,
                                               diff=diff,
                                               limit=limit,
                                               remove_swords=remove_swords)

    analysis = analysis_query.get()
    analysis.by_metadata = by_metadata_results
    analysis.save()

    # TENTATIVE! Debating whether or not to return the dictionary or the whole model to the view
    return by_metadata_results


def by_overlap(corpus_id,word_window):
    """
    Looks through the gendered words across the corpus and extracts words that overlap
    across all genders and their occurrences sorted.

    :param corpus_id: An int representing a `Corpus` instance
    :param word_window: An integer describing the number of words to look at of each side of a gendered word

    :return: {str: [gender1, gender2, ...], ...}
    """

    output = {}

    analysis_query = ProximityAnalyses.objects.filter(
        corpus__pk='corpus_id',
        word_window=word_window
    )

    if not analysis_query.filter(by_overlap=dict()).exists():
        return analysis_query.values_list('by_overlap', flat=True).get()

    sets_of_adjectives = {}

    all_gender_labels = Gender.objects.values_list('label', flat=True)

    for gender_label in all_gender_labels:
        sets_of_adjectives[gender_label] = set(list(by_gender()[gender_label].keys()))

    intersects_with_all = set.intersection(*sets_of_adjectives.values())

    for adj in intersects_with_all:
        results_by_gender = {}
        for gender_label in all_gender_labels:
            results_by_gender[gender_label] = by_gender().get(gender_label).get(adj)
        output[adj] = results_by_gender

    analysis = analysis_query.get()
    analysis.by_overlap = output
    analysis.save()

    return output


def apply_result_filters(key_gender_token_counters, diff, sort, limit, remove_swords):
    """
    A helper function for applying optional keyword arguments to the output of
    GenderProximityAnalysis methods, allowing the user to sort, diff, limit, and remove stopwords
    from the output. These transformations do not mutate the input.

    :param key_gender_token_counters: a dictionary shaped Dict[Union[str, int], GenderTokenCounters]
    :param diff: return the difference in token occurrences across Genders.
    :param sort: return an array of the shape Sequence[Tuple[str, int]]
    :param limit: if sort==True, return only n=limit token occurrences.
    :param remove_swords: remove stop words from output.

    :return: a dictionary of the shape Dict[Union[str, int], GenderTokenResponse]
    """

    output = {}
    for key, gender_token_counters in key_gender_token_counters.items():
        if remove_swords:
            output[key] = remove_swords(gender_token_counters)
        else:
            output[key] = gender_token_counters

        if diff:
            output[key] = diff_gender_token_counters(output[key])

        if sort:
            output[key] = sort_gender_token_counters(output[key], limit=limit)

    return output


def diff_gender_token_counters(gender_token_counters):
    """
    A helper function that determines the difference of token occurrences
    across multiple Genders.
    :param gender_token_counters: Dict[str, Counter]
    >>> token_frequency_1 = Counter({'foo': 1, 'bar': 2, 'baz': 4})
    >>> token_frequency_2 = Counter({'foo': 2, 'bar': 3, 'baz': 2})
    >>> test = {'Male': token_frequency_1, 'Female': token_frequency_2}
    >>> _diff_gender_token_counters(test).get('Male')
    Counter({'baz': 2, 'foo': -1, 'bar': -1})
    """

    difference_dict = {}

    for gender in gender_token_counters:
        current_difference = Counter()

        for word, count in gender_token_counters[gender].items():
            current_difference[word] = count

        for other_gender in gender_token_counters:
            if other_gender == gender:
                continue
            other_adjective_frequency = gender_token_counters[other_gender]

            for word, count in other_adjective_frequency.items():
                if word in current_difference.keys():
                    current_difference[word] -= count

        difference_dict[gender] = current_difference

    return difference_dict


def remove_swords(gender_token_counters):
    """
    A helper function for removing stop words from a GenderTokenCounters dictionary.
    :param gender_token_counters: Dict[str, Counter].
    :return: GenderTokenCounters.
    >>> token_frequency_1 = Counter({'foo': 1, 'bar': 2, 'bat': 4})
    >>> token_frequency_2 = Counter({'foo': 2, 'baz': 3, 'own': 2})
    >>> test = {'Male': token_frequency_1, 'Female': token_frequency_2}
    >>> _remove_swords(test).get('Male').get('own') is None
    True
    """
    output = {}
    swords_eng_set = set(SWORDS_ENG)
    for gender_label, token_counter in gender_token_counters.items():
        sanitized_counter = Counter()
        for token, count in token_counter.items():
            if token in swords_eng_set:
                continue
            sanitized_counter[token] = count
        output[gender_label] = sanitized_counter
    return output


def sort_gender_token_counters(gender_token_counters,
                               limit):
    """
    A helper function for transforming a dictionary of token instances keyed by
    Gender.label into a sorted list of tuples.
    :param gender_token_counters: Dict[str, Counter].
    :param limit: Optional[int], if sort=True, return n=limit number of items in descending order
    :return: Dict[str, Sequence[Tuple[str, int]]]
    >>> token_frequency_1 = Counter({'foo': 1, 'bar': 2, 'bat': 4})
    >>> token_frequency_2 = Counter({'foo': 2, 'baz': 3})
    >>> test = {'Male': token_frequency_1, 'Female': token_frequency_2}
    >>> _sort_gender_token_counters(test).get('Male')
    [('bat', 4), ('bar', 2), ('foo', 1)]
    >>> _sort_gender_token_counters(test).get('Female')
    [('baz', 3), ('foo', 2)]
    >>> _sort_gender_token_counters(test, limit=1).get('Male')
    [('bat', 4)]
    >>> _sort_gender_token_counters(test, limit=2).get('Male')
    [('bat', 4), ('bar', 2)]
    """
    output_gender_token_counters = {}

    for gender, token_counter in gender_token_counters.items():
        output_gender_token_counters[gender] = {}
        output_gender_token_counters[gender] = token_counter.most_common(limit)

    return output_gender_token_counters


def merge_token_counters(token_counters):
    """
    A helper function for combining multiple dictionaries of the shape token_frequency
    into a single token_frequency.
    :param token_counters: a list of the shape [{str: int, ...}, ...]
    :return: a dictionary of the same shape as the above, with all key: value pairs merged.
    >>> test_1 = Counter({'good': 1, 'bad': 1, 'ugly': 1})
    >>> test_2 = Counter({'good': 3, 'bad': 0, 'weird': 2})
    >>> test_3 = Counter({'good': 2, 'bad': 4, 'weird': 0, 'ugly': 2})
    >>> merged_token_frequency = _merge_token_counters([test_1, test_2, test_3])
    >>> merged_token_frequency
    Counter({'good': 6, 'bad': 5, 'ugly': 3, 'weird': 2})
    """
    return reduce(lambda token_counter, total: token_counter + total, token_counters)


def run_analysis(corpus_id, word_window):
    """
    Generates a dictionary of dictionaries for each `Document` object. Each dictionary maps a `Gender` to a word count
    of words within a specified window of that `Gender`'s pronouns.
    :param corpus_id: An int representing a `Corpus` instance
    :param word_window: An integer describing the number of words to look at of each side of a gendered word
    :return: A dict mapping `Document` ids to a dict mapping strings (`Gender` labels) to a `Counter` instance.
    """

    analysis_cache = ProximityAnalyses.objects.filter(corpus__pk=corpus_id, word_window=word_window)
    if analysis_cache.exists():
        return analysis_cache[0]

    results = {}
    doc_ids = Corpus.objects.filter(pk=corpus_id).values_list('documents__pk', flat=True)

    for key in doc_ids:
        results[key] = _generate_gender_token_counters(
            Document.objects.values_list('tokenized_text', flat=True).filter(pk=key), word_window)

    analysis = ProximityAnalyses.objects.create(results=results, word_window=word_window)

    corpus_query = Corpus.objects.filter(pk=corpus_id)
    analysis.corpus = corpus_query.get()
    analysis.save()

    return analysis


def _generate_gender_token_counters(text_query, word_window):
    """
    A private function generating a dictionary mapping `Gender`s to a word count of words within a specified window of the `Gender`'s
    pronouns.

    :param text_query: An unevaluated, length-1 `QuerySet` that returns a list of strings when evaluated
    :param word_window: An integer describing the number of words to look at of each side of a gendered word

    :return: A dict mapping strings (`Gender` labels) to a `Counter` instance.
    """

    results = {}
    gender_ids = Gender.objects.values_list('pk', flat=True)

    for gender_id in gender_ids:
        gender = Gender.objects.get(pk=gender_id)

        doc_result = _generate_token_counter(text_query, gender, word_window)
        results[gender.label] = doc_result

    return results


def _generate_token_counter(text_query, gender, word_window):
    # pylint: disable=too-many-locals
    """
    A private function generating a 'Counter' instance mapping words to their frequency within a text.

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
