import math
from collections import Counter

from ..models import Corpus


####################
# HELPER FUNCTIONS #
####################


def _get_wordcount_counter(corpus: Corpus):
    """
    This function returns a Counter object that stores
    how many times each word appears in the corpus.
    :return: Python Counter object
    """
    corpus_counter = Counter()
    for document in corpus.documents.all():
        document_counter = document.word_count_counter
        corpus_counter += document_counter
    return corpus_counter


def dunn_individual_word(total_words_in_corpus_1,
                         total_words_in_corpus_2,
                         count_of_word_in_corpus_1,
                         count_of_word_in_corpus_2):
    """
    applies Dunning log likelihood to compare individual word in two counter objects

    :param total_words_in_corpus_1: int, total wordcount in corpus 1
    :param total_words_in_corpus_2: int, total wordcount in corpus 2
    :param count_of_word_in_corpus_1: int, wordcount of one word in corpus 1
    :param count_of_word_in_corpus_2: int, wordcount of one word in corpus 2
    :return: Float representing the Dunning log likelihood of the given inputs

    >>> total_words_m_corpus = 8648489
    >>> total_words_f_corpus = 8700765
    >>> wordcount_female = 1000
    >>> wordcount_male = 50
    >>> dunn_individual_word(total_words_m_corpus,
    ...                      total_words_f_corpus,
    ...                      wordcount_male,
    ...                      wordcount_female)
    -1047.8610274053995

    """
    # NOTE(ra): super short var names actually useful here for reading the math
    # pylint: disable=invalid-name

    a = count_of_word_in_corpus_1
    b = count_of_word_in_corpus_2
    c = total_words_in_corpus_1
    d = total_words_in_corpus_2

    e1 = c * (a + b) / (c + d)
    e2 = d * (a + b) / (c + d)

    dunning_log_likelihood = 2 * (a * math.log(a / e1) + b * math.log(b / e2))

    if count_of_word_in_corpus_1 * math.log(count_of_word_in_corpus_1 / e1) < 0:
        dunning_log_likelihood = -dunning_log_likelihood

    return dunning_log_likelihood


def dunning_total(corpus_1, corpus_2):
    """
    Runs dunning_individual on words shared by both Corpus objects
    (-) end of spectrum is words for corpus_2
    (+) end of spectrum is words for corpus_1
    the larger the magnitude of the number, the more distinctive that word is in its
    respective Corpus object

    :param corpus_1: Python Corpus object
    :param corpus_2: Python Corpus object
    :return: Dictionary of the form
        {"unique to corp 1": {word1, word2, word3, ...},
        "unique to corp 2": {word1, word2, word3, ...},
        "common words": {word1: {dunning score, count1, count2}, word2: {dunning score, count1, count 2}, ...}}
    """
    counter_1 = _get_wordcount_counter(corpus_1)
    counter_2 = _get_wordcount_counter(corpus_2)

    total_word_count_1 = sum(counter_1.values())
    total_word_count_2 = sum(counter_2.values())

    assert total_word_count_1 > 0 or total_word_count_2 > 0, "One or more corpora is empty"

    # dictionary where results will be returned
    result = {"unique_to_corp_1": set(),
              "unique_to_corp_2": set(),
              "common_words": {}}

    for word in counter_1:
        counter1_wordcount = counter_1[word]
        try:
            counter2_wordcount = counter_2[word]

            dunning_word = dunn_individual_word(total_word_count_1,
                                                total_word_count_2,
                                                counter1_wordcount,
                                                counter2_wordcount)

            result["common_words"][word] = {
                'dunning': dunning_word,
                'count_corp1': counter1_wordcount,
                'count_corp2': counter2_wordcount
            }
        except ValueError:  # if word is not in counter_2
            result["unique_to_corp_1"].add(word)

    # consider words unique to corpus_2
    for word in counter_2:
        if word not in counter_1:
            result["unique_to_corp_2"].add(word)

    return result
