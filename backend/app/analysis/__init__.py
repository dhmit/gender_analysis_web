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
    Runs _generate_gender_token_counters across each document in the corpus
    For optimization version: `doc_set` is a `QuerySet` of `Document` objects.
    """
    results = {}

    for doc in doc_set.values('pk', 'tokenized_text'):
        results['pk'] = 'tokenized_text'
        del results['pk']

    print('END run_analysis')
    return results
