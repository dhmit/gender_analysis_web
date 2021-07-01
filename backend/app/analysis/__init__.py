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

    for doc in doc_set.values('pk', 'tokenized_text'):
        results['pk'] = 'tokenized_text'
        del results['pk']

    print('END run_analysis')
    return results
