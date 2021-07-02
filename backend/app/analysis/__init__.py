from memory_profiler import profile
from django.db import connection
from app.models import Document


def longfrock():
    return open('app/analysis/aanrud_longfrock.txt').read()


def make_documents(num):
    """
    Mechanism (mainly for debugging) for creating test `Document` objects.
    Each `Document` here holds about 2 KB of text.

    :param: num: A nonnegative `int` representing the number of `Document`s to be created and saved to the database.
    :return: `None`
    """
    assert num >= 0, 'Please input a nonnegative integer.'

    for _ in range(num):
        Document.objects.create(author='Hans Aanrud', text=longfrock())

    print(f'Done! {num} Document objects created.\nTotal number of Document objects: {Document.objects.count()}')


@profile
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

    cursor = connection.cursor()
    input_query = str(doc_set.only('tokenized_text').query).replace('\"', '')
    query = f"DECLARE doc_cursor BINARY CURSOR FOR {input_query}"
    breakpoint()

    cursor.execute(query)
    cursor.execute('OPEN doc_cursor')

    while True:
        doc_subset = cursor.execute('FETCH 10 FROM doc_cursor')
        for _ in range(10):
            doc = doc_subset.fetchone()
            breakpoint()

    # query = doc_set.only('tokenized_text').iterator()

    # for doc in query:
    #     results['pk'] = 'tokenized_text'
    #     del results['pk']

    print('END run_analysis')
    return results
