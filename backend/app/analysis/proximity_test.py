from ..models import Document, Corpus
from rest_framework.test import APIRequestFactory
from app.views import add_proximity_analysis


def proximity_view_test(text):
    """A function for testing the proximity analysis posting,
    check api/all_proximity to see the updates list
    """
    c1 = Corpus(title="Corpus Test", description="This is the testing corpus")
    c1.save()
    Document.objects.create_document(title='document_1', year=2021, text=text)
    d1 = Document.objects.get(title='document_1')
    c1.documents.add(d1)
    factory = APIRequestFactory()
    request = factory.post('api/all_proximity', {'word_window': '2', 'corpus_id': c1.id})
    add_proximity_analysis(request)

