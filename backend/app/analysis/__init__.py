import gc

from django.db import connection
from memory_profiler import profile

from app.models import Document


def longfrock():
    """
    Returns a relatively small text sample used for optimizing and debugging `Document` iteration.
    :return: Around 2 KB of text as a string.
    """
    return open('app/analysis/aanrud_longfrock.txt').read()


def middlemarch():
    """
    Returns a relatively large text sample used for optimizing and debugging `Document` iteration.
    :return: Around 1.7 MB of text as a string.
    """
    return open('app/analysis/eliot_middlemarch.txt').read()


def professor():
    """
    Returns a relatively medium-sized text sample used for optimizing and debugging `Document` iteration.
    :return: Around 5 KB of text as a string.
    """
    return open('app/analysis/bronte_professor.txt').read()

@profile
def make_documents_wrapper(num, text_func):
    @profile
    def make_documents(num, text_func):
        """
        Mechanism (mainly for debugging) for creating test `Document` objects.

        :param num: A non-negative `int` representing the number of `Document`s to be created and saved to the database.
        :param text_func: A function that returns a sample of text as a string.
        :return: `None`
        """
        assert num >= 0, 'Please input a non-negative integer.'

        for _ in range(num):
            Document.objects.create_document(text=text_func())

        print(f'Done! {num} Document objects created.\nTotal number of Document objects: {Document.objects.count()}')
        gc.collect()

    make_documents(num, text_func)
    print('Anything happen?')


@profile
def run_analysis(doc_set):
    """
    A test version of the `run_analysis` method found in the `GenderProximityAnalyzer` class in `proximity.py`.
    Focuses on optimizing iteration through a `QuerySet` of Documents. This uses the `results` dictionary to trigger
    evaluation of the `doc_set` `QuerySet`.

    For more on `QuerySet` evaluation, see https://docs.djangoproject.com/en/3.1/topics/db/queries/#querysets-are-lazy.

    :param doc_set: A `QuerySet` of `Document` objects.
    :return: An empty dict
    """

    # results = {}

    # ------- SQLite3 doesn't support the 'DECLARE' or 'FETCH' keywords! (https://www.sqlite.org/lang_keywords.html)
    # ------- It also doesn't support cursors -- we need another solution.
    # cursor = connection.cursor()
    # input_query = str(doc_set.only('tokenized_text').query).replace('\"', '')
    # query = f"DECLARE doc_cursor BINARY CURSOR FOR {input_query}"
    #
    # breakpoint()  # Works fine up to here
    #
    # cursor.execute(query)  # Here's the error
    # cursor.execute('OPEN doc_cursor')
    #
    # while True:
    #     doc_subset = cursor.execute('FETCH 10 FROM doc_cursor')
    #     for _ in range(10):
    #         doc = doc_subset.fetchone()
    #         breakpoint()
    print(len(connection.queries))

    # query = doc_set
    query = doc_set.iterator()
    # query = doc_set.only('tokenized_text')
    # query = doc_set.only('tokenized_text').iterator()

    # i = 0
    for doc in query:
        pass
        print('\nQuery count:', len(connection.queries))
        # results[doc.pk] = doc.tokenized_text
        # print('After adding to dict:', len(connection.queries))
        # i += 1

    print(f'\nEND run_analysis')
    return None

@profile
def analysis_wrapper(doc_set):
    """
    A debugging function to mimic the analysis performed on a `QuerySet` of `Document` objects in an analysis function.
    Uses a wrapper function to track changes in memory usage over time, including after the function call (to track
    garbage collection).

    For more on `QuerySet` evaluation, see https://docs.djangoproject.com/en/3.1/topics/db/queries/#querysets-are-lazy.

    :param doc_set: A `QuerySet` of `Document` objects. This `QuerySet` should come unevaluated (can check this using
        QuerySet._result_cache. If this cache is empty, the `QuerySet` was likely never evaluated.

    :return: A string ("Done!") to signal completion when running this in the Django shell (python manage.py shell).
    """

    # define a function, and inside of it:
    #   iterate through the Query Set
    #   run analysis on it (for now, create a word count dictionary without using Document.word_count attribute)
    #   return the word counts dictionary
    # do something relevant to seeing the memory usage/tracking garbage collection of `Document` instances
    # return the results dictionary

    @profile
    def doc_iteration(doc_set):
        """
        Iterate through the `Document` objects, create master word_count dictionary

        :param doc_set: A `QuerySet` (unevaluated) of `Document` objects. This could come from, for example, a
            `corpus.documents.all()` call on a `Corpus` instance or a `Document.objects.all()` call (as long as the
            `QuerySet` would return `Document` objects when evaluated.
        :return: A word count dictionary using data from all `Document`s in the `QuerySet`.
        """
        results = {}

        for key in doc_set.values_list('pk', flat=True):
            doc_text_query = doc_set.values_list('tokenized_text', flat=True).filter(pk=key)
            # breakpoint()

            results.update(get_analysis(doc_text_query))

        return results

    @profile
    def get_analysis(doc_text_query):
        """
        Create a word count dictionary for a tokenized text

        :param doc_text_query: A length-1 (unevaluated) `QuerySet` object that, when evaluated, returns a list
            of strings.
        :return: A dictionary mapping strings (tokens) to ints (frequency).
        """
        assert doc_text_query.count() == 1, 'Something went wrong with filtering the `QuerySet`!'

        results = {}

        # Finally hits the database (once) and loads the tokenized_text field as a list of strings
        # The .get() method does not cache (store) the results.
        for word in doc_text_query.get():
            results[word] = results.get(word, 0) + 1

        # After the function returns the results dict, the list of strings object is destroyed (exactly what we want!)
        # and Python frees up memory for the next list of strings (the next function call; the next iteration)
        return results

    results_dict = doc_iteration(doc_set)
    print('Queries:\n', connection.queries, sep='')
    return "Done!"

