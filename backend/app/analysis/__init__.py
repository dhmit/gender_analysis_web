from django.db import connection
from memory_profiler import profile

from app.models import Document


def longfrock():
    return open('app/analysis/aanrud_longfrock.txt').read()

def middlemarch():
    return open('app/analysis/eliot_middlemarch.txt').read()


@profile
def make_documents(num):
    """
    Mechanism (mainly for debugging) for creating test `Document` objects.
    Each `Document` here holds about 2 KB of text.

    :param: num: A non-negative `int` representing the number of `Document`s to be created and saved to the database.
    :return: `None`
    """
    assert num >= 0, 'Please input a non-negative integer.'

    for _ in range(num):
        Document.objects.create(author='George Eliot', title='Middlemarch', text=middlemarch())

    print(f'Done! {num} Document objects created.\nTotal number of Document objects: {Document.objects.count()}')


# @profile
def run_analysis(doc_set):
    """
    A test version of the `run_analysis` method found in the `GenderProximityAnalyzer` class in `proximity.py`.
    Focuses on optimizing iteration through a `QuerySet` of Documents. This uses the `results` dictionary to trigger
    evaluation of the `doc_set` `QuerySet`.

    For more on `QuerySet` evaluation, see https://docs.djangoproject.com/en/3.1/topics/db/queries/#querysets-are-lazy.

    :param: doc_set: A `QuerySet` of `Document` objects.
    :return: An empty dict
    """
    results = {}
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
    query = doc_set.only('tokenized_text').iterator()
    print('After iterator declaration:', len(connection.queries))

    for doc in query:
        print('\nBefore adding to dict:', len(connection.queries))
        results[doc.pk] = doc.tokenized_text
        print('After adding to dict:', len(connection.queries))

    print('\nEND run_analysis')
    return {}
