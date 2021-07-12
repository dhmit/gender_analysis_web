"""
These view functions and classes implement both standard GET routes and API endpoints.

GET routes produce largely empty HTML pages that expect a React component to attach to them and handle most view
concerns. You can supply a few pieces of data in the render function's context argument to support this expectation.

Of particular use are the properties: page_metadata, component_props, and component_name:
page_metadata: these values will be included in the page's <head> element. Currently, only the `title` property is used.
component_props: these can be any properties you wish to pass into your React components as its highest-level props.
component_name: this should reference the exact name of the React component you intend to load onto the page.

Example:
context = {
    'page_metadata': {
        'title': 'Example ID page'
    },
    'component_props': {
        'id': example_id
    },
    'component_name': 'ExampleId'
}
"""
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import (
    Document,
    Gender,
    Corpus
)
from .serializers import (
    DocumentSerializer,
    SimpleDocumentSerializer,
    GenderSerializer,
    CorpusSerializer
)


@api_view(['GET'])
def get_example(request, example_id):
    """
    API example endpoint.
    """

    data = {
        'name': 'Example',
        'id': example_id,
    }
    return Response(data)


def index(request):
    """
    Home page
    """

    context = {
        'page_metadata': {
            'title': 'Home page'
        },
    }

    return render(request, 'index.html', context)


def example(request):
    """
    Example page
    """

    context = {
        'page_metadata': {
            'title': 'Example page'
        },
    }

    return render(request, 'index.html', context)


def example_id(request, example_id):
    """
    Example ID page
    """

    context = {
        'page_metadata': {
            'title': 'Example ID page'
        },
        'component_props': {
            'id': example_id
        },
        'component_name': 'ExampleId'
    }

    return render(request, 'index.html', context)


@api_view(['POST'])
def add_document(request):
    """
    API endpoint for adding a piece of document
    """
    attributes = request.data
    fields = {
        'title': attributes['title'],
        'author': attributes['author'],
        'year': attributes['year'] if attributes['year'] != '' else None,
        'text': attributes['text']
    }
    new_text_obj = Document.objects.create_document(**fields)
    serializer = DocumentSerializer(new_text_obj)
    return Response(serializer.data)


@api_view(['GET'])
def all_documents(request):
    """
    API Endpoint to get all the documents
    """
    doc_objs = Document.objects.all()
    serializer = SimpleDocumentSerializer(doc_objs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_document(request, doc_id):
    """
    API Endpoint to get a document based on the ID
    """
    doc_obj = Document.objects.get(id=doc_id)
    serializer = DocumentSerializer(doc_obj)
    return Response(serializer.data)


def documents(request):
    """
    All Documents page
    """

    context = {
        'page_metadata': {
            'title': 'Documents'
        },
        'component_name': 'Documents'
    }

    return render(request, 'index.html', context)


def single_document(request, doc_id):
    """
    Single Document page
    """

    context = {
        'page_metadata': {
            'title': 'Document '
        },
        'component_props': {
            'id': doc_id
        },
        'component_name': 'SingleDocument'
    }

    return render(request, 'index.html', context)


@api_view(['GET'])
def all_genders(request):
    """
    API Endpoint to get all gender instances.
    """
    gender_objs = Gender.objects.all()
    serializer = GenderSerializer(gender_objs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_corpus(request):
    """
    API endpoint for adding a corpus instance
    """
    attributes = request.data
    fields = {
        'title': attributes['title'],
        'description': attributes['description']
    }
    new_corpus_obj = Corpus.objects.create(**fields)
    serializer = CorpusSerializer(new_corpus_obj)
    return Response(serializer.data)


@api_view(['POST'])
def update_corpus_docs(request):
    """
    API endpoint for updating the documents in a corpus
    """
    corpus_data = request.data
    corpus_id = corpus_data['id']
    docs_list = corpus_data['documents']
    corpus_obj = Corpus.objects.get(id=corpus_id)
    corpus_obj.documents.set(docs_list)
    serializer = CorpusSerializer(corpus_obj)
    return Response(serializer.data)


@api_view(['GET'])
def all_corpora(request):
    """
    API Endpoint to get all the corpora
    """
    corpus_objs = Corpus.objects.all()
    serializer = CorpusSerializer(corpus_objs, many=True)
    return Response(serializer.data)


def corpora(request):
    """
    Corpora page
    """

    context = {
        'page_metadata': {
            'title': 'Corpora'
        },
        'component_name': 'Corpora'
    }

    return render(request, 'index.html', context)
