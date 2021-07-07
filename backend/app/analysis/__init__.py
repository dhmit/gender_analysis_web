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
    This was an early version of testing out `Document` iteration by iterating through an entirely loaded list of
    `Document` objects (with variations). This method proved to be ineffective in favor of the method outlined in
    `analysis_wrapper` below. I've left the method here in case any of these notes are of any value.

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

    # Four variations of queries. The ones with .iterator() attached evaluate the `QuerySet` immediately, load all
    # objects from the database, and return an iterator object. This method does not populate the cache of the original
    # 'QuerySet', but the method still proved ineffective (for reasons I have't yet figured out, it actually didn't
    # seem to help memory usage at all. It's probably because if the original doc_set parameter is filtered or
    # modified in any way, the doc_set `QuerySet` will never have its `._result_cache` populated (since filtering a
    # `QuerySet` returns another `QuerySet`, for the most part.

    # For more details on `QuerySet`s, check out Django's API reference:
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#methods-that-do-not-return-querysets


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
        QuerySet._result_cache. If this cache is empty, the `QuerySet` was likely never evaluated).

    :return: A string ("Done!") to signal completion when running this in the Django shell (`python manage.py shell`).
    """

    # define a function, and inside of it:
    #   iterate through the Query Set
    #   run analysis on it (for now, create a word count dictionary without using Document.word_count attribute)
    #   return the word counts dictionary
    # do something relevant to seeing the memory usage/tracking garbage collection of `Document` instances
    #   (here the "something relevant" is splitting the above steps into several functions to try and track memory usage
    #   across scopes/local environments and any object destruction)
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
            # breakpoint() - we want to make sure this is an unevaluted `QuerySet`.
            # Maybe there's a way to do this passing in only the *primary key* down to the get_analysis function.
            # After all, an int takes up less space than a `QuerySet`!

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

