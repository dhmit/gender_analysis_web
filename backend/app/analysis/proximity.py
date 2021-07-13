import nltk
from collections import Counter
from more_itertools import windowed
from functools import reduce
from ..common import compute_bin_year, SWORDS_ENG

from ..models import (
    Document,
    Gender,
    Corpus,
)


def by_date(corpus_id,
            time_frame,
            bin_size,
            sort,
            diff,
            limit,
            remove_swords):


    output = {}
    # Results is the model for persistence of anaylsis results 
    # Results model to be finalized
    results = Results.objects.all()[-1].results_dict
    
    all_gender_labels = [each_gender.label for each_gender in list(Gender.objects.all())]

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
                [results[each_id][gender_label], output[bin_year][gender_label]]
            )

    return apply_result_filters(output,
                                 sort=sort,
                                 diff=diff,
                                 limit=limit,
                                 remove_swords=remove_swords)

def by_document(
                sort,
                diff,
                limit,
                remove_swords):

    """
    Return analysis organized by Document.
    :param sort: Optional[bool], return Dict[int, Sequence[Tuple[str, int]]]
    :param diff: return the differences between genders.
    :param limit: Optional[int], if sort=True, return n=limit number of items in desc order.
    :param remove_swords: Optional[bool], remove stop words from return
    :return: a dictionary of the shape { str(Gender.label): { str(token): int } } or
             { str(Gender.label): [(str(token), int)] }
    >>> from gender_analysis.testing.common import DOCUMENT_TEST_PATH, DOCUMENT_TEST_CSV
    >>> from gender_analysis import Corpus
    >>> analyzer = GenderProximityAnalyzer(file_path=DOCUMENT_TEST_PATH,
    ...                                    csv_path=DOCUMENT_TEST_CSV)
    >>> doc = analyzer.corpus.documents[7]
    >>> analyzer_document_labels = list(analyzer.by_document().keys())
    >>> document_labels = list(map(lambda d: d.label, analyzer.corpus.documents))
    >>> analyzer_document_labels == document_labels
    True
    >>> analyzer.by_document().get(doc.label)
    {'Female': Counter({'sad': 6, 'died': 1}), 'Male': Counter()}
    """

    output = {}

    # Results is the model for persistence of anaylsis results
    results = Results.objects.all()[-1].results_dict

    for document_id in results:
        output[Document.objects.values_list('title', flat=True).filter(pk=document_id)] = results[document_id]

    return apply_result_filters(output,
                                 sort=sort,
                                 diff=diff,
                                 limit=limit,
                                 remove_swords=remove_swords)

def by_gender(
              sort,
              diff,
              limit,
              remove_swords):
    """
    Return analysis organized by Document. Merges all words across texts
    into dictionaries sorted by gender.
    :param sort: Optional[bool], return Dict[str, Sequence[Tuple[str, int]]]
    :param diff: return the differences between genders.
    :param limit: Optional[int], if sort=True, return n=limit number of items in desc order.
    :param remove_swords: Optional[bool], remove stop words from return
    :return: a dictionary of the shape {Gender.label: {str: int, ...}, ...}
    >>> from gender_analysis.testing.common import DOCUMENT_TEST_PATH, DOCUMENT_TEST_CSV
    >>> from gender_analysis import Corpus
    >>> analyzer = GenderProximityAnalyzer(file_path=DOCUMENT_TEST_PATH,
    ...                                    csv_path=DOCUMENT_TEST_CSV)
    >>> analyzer.by_gender().keys()
    dict_keys(['Female', 'Male'])
    >>> analyzer.by_gender().get('Female')
    Counter({'sad': 14, 'beautiful': 3, 'died': 1})
    >>> analyzer.by_gender(sort=True).get('Female')
    [('sad', 14), ('beautiful', 3), ('died', 1)]
    >>> analyzer.by_gender(diff=True).get('Female')
    Counter({'beautiful': 3, 'died': 1, 'sad': 0})
    >>> analyzer.by_gender(diff=True, sort=True).get('Female')
    [('beautiful', 3), ('died', 1), ('sad', 0)]
    """

    hashed_arguments = f"{str(sort)}{str(diff)}{str(limit)}{remove_swords}"

    all_stored_hashed_arguments = Results.objects.values_list('gender_hashed_arguments', flat=True)

    if hashed_arguments in all_stored_hashed_arguments:
        return all_stored_hashed_arguments[hashed_arguments]

    merged_results = {}
    all_gender_labels = [each_gender.label for each_gender in list(Gender.objects.all())]

    # Results is the model for persistence of anaylsis results
    results = Results.objects.all()[-1].results_dict

    for gender_label in all_gender_labels:
        new_gender_token_counters = [
            results[document_id][gender_label] for document_id in results
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

    return output

def by_metadata(
                metadata_field,
                sort,
                diff,
                limit,
                remove_swords):
    """
    Return analysis organized by Document metadata. Merges all words across texts
    into dictionaries sorted by provided metadata_key.
    :param metadata_key: a string.
    :param sort: Optional[bool], return Dict[str, Sequence[Tuple[str, int]]]
    :param diff: return the differences between genders.
    :param limit: Optional[int], if sort=True, return n=limit number of items in desc order.
    :param remove_swords: Optional[bool], remove stop words from return
    :return: a dictionary of the shape {Gender.label: {str: int , ...}, ...}.
    >>> from gender_analysis.testing.common import DOCUMENT_TEST_PATH, DOCUMENT_TEST_CSV
    >>> from gender_analysis import Corpus
    >>> analyzer = GenderProximityAnalyzer(file_path=DOCUMENT_TEST_PATH,
    ...                                    csv_path=DOCUMENT_TEST_CSV)
    >>> analyzer.by_metadata('author_gender').keys()
    dict_keys(['male', 'female'])
    >>> analyzer.by_metadata('author_gender').get('female')
    {'Female': Counter({'sad': 7}), 'Male': Counter({'sad': 12, 'deep': 1})}
    >>> analyzer.by_metadata('author_gender', sort=True).get('female')
    {'Female': [('sad', 7)], 'Male': [('sad', 12), ('deep', 1)]}
    >>> analyzer.by_metadata('author_gender', diff=True).get('female')
    {'Female': Counter({'sad': -5}), 'Male': Counter({'sad': 5, 'deep': 1})}
    """

    output = {}

    # Results is the model for persistence of anaylsis results
    results = Results.objects.all()[-1].results_dict

    all_gender_labels = [each_gender.label for each_gender in list(Gender.objects.all())]

    for document_id, gender_token_counters in results.items():
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

    return apply_result_filters(output,
                                 sort=sort,
                                 diff=diff,
                                 limit=limit,
                                 remove_swords=remove_swords)

def by_overlap():
    """
    Looks through the gendered words across the corpus and extracts words that overlap
    across all genders and their occurrences sorted.
    :return: {str: [gender1, gender2, ...], ...}
    >>> from gender_analysis.testing.common import DOCUMENT_TEST_PATH, DOCUMENT_TEST_CSV
    >>> from gender_analysis import Corpus
    >>> analyzer = GenderProximityAnalyzer(file_path=DOCUMENT_TEST_PATH,
    ...                                    csv_path=DOCUMENT_TEST_CSV)
    >>> analyzer.by_overlap()
    {'sad': {'Female': 14, 'Male': 14}}
    """

    output = {}
    sets_of_adjectives = {}

    all_gender_labels = [each_gender.label for each_gender in list(Gender.objects.all())]

    for gender_label in all_gender_labels:
        sets_of_adjectives[gender_label] = set(list(by_gender()[gender_label].keys()))

    intersects_with_all = set.intersection(*sets_of_adjectives.values())

    for adj in intersects_with_all:
        results_by_gender = {}
        for gender_label in all_gender_labels:
            results_by_gender[gender_label] = by_gender().get(gender_label).get(adj)
        output[adj] = results_by_gender

    return output

def apply_result_filters(key_gender_token_counters,diff,sort,limit,remove_swords):
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
    >>> test_counter_1 = Counter({'foo': 1, 'bar': 2, 'own': 2})
    >>> test_counter_2 = Counter({'foo': 5, 'baz': 2})
    >>> test = {'doc': {'Male': test_counter_1, 'Female': test_counter_2}}
    >>> _apply_result_filters(test, diff=True, sort=False, limit=10, remove_swords=False).get('doc')
    {'Male': Counter({'bar': 2, 'own': 2, 'foo': -4}), 'Female': Counter({'foo': 4, 'baz': 2})}
    >>> _apply_result_filters(test, diff=False, sort=True, limit=10, remove_swords=False).get('doc')
    {'Male': [('bar', 2), ('own', 2), ('foo', 1)], 'Female': [('foo', 5), ('baz', 2)]}
    >>> _apply_result_filters(test, diff=False, sort=False, limit=10, remove_swords=True).get('doc')
    {'Male': Counter({'bar': 2, 'foo': 1}), 'Female': Counter({'foo': 5, 'baz': 2})}
    >>> _apply_result_filters(test, diff=True, sort=True, limit=10, remove_swords=False).get('doc')
    {'Male': [('bar', 2), ('own', 2), ('foo', -4)], 'Female': [('foo', 4), ('baz', 2)]}
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
        results[key] = generate_gender_token_counters(
            Document.objects.values_list('tokenized_text', flat=True).filter(pk=key),
            gender_ids,
            word_window
        )

    return results


def generate_gender_token_counters(text_query, gender_ids, word_window):
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

        doc_result = generate_token_counter(text_query, gender, word_window)
        results[gender.label] = doc_result

    return results


def generate_token_counter(text_query, gender, word_window):
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
