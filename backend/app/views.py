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
import csv


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
from app.services.parse_csv import parse_csv

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
    print("we are in add_document")
    attributes = request.data
    new_attributes = {}
    for attribute in attributes['newAttributes']:
        key, value = attribute['name'], attribute['value']
        if key and value:
            new_attributes[key] = value
    fields = {
        'title': attributes['title'],
        'author': attributes['author'],
        'year': attributes['year'] if attributes['year'] != '' else None,
        'text': attributes['text'],
        'new_attributes': new_attributes
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

@api_view(['POST'])
def upload_document(request):
    """
    API endpoint for uploading csv files that are to be converted to an instance of csv_reader
    """

    file = request.data["filename"]

    content = file.read().decode('utf-8').splitlines()
    csv_reader = csv.DictReader(content)
    new_corpus = parse_csv(csv_reader)
    serializer = CorpusSerializer(new_corpus)
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
    doc_ids = corpus_data['documents']
    corpus_obj = Corpus.objects.get(id=corpus_id)
    corpus_obj.documents.set(Document.objects.filter(id__in=doc_ids))
    serializer = CorpusSerializer(corpus_obj)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_corpus(request):
    """
    API endpoint for deleting a corpus
    """
    corpus_id = request.data['id']
    corpus_obj = Corpus.objects.get(id=corpus_id)
    res = corpus_obj.delete()
    return Response(res)


@api_view(['GET'])
def all_corpora(request):
    """
    API endpoint to get all the corpora
    """
    corpus_objs = Corpus.objects.all()
    serializer = CorpusSerializer(corpus_objs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_corpus(request, corpus_id):
    """
    API endpoint to get a corpus based on id
    """
    corpus_obj = Corpus.objects.get(id=corpus_id)
    serializer = CorpusSerializer(corpus_obj)
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


def corpus(request, corpus_id):
    """
    Corpus Page
    """

    context = {
        'page_metadata': {
            'title': 'Corpus'
        },
        'component_props': {
            'id': corpus_id
        },
        'component_name': 'Corpus'
    }

    return render(request, 'index.html', context)
    
