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
    Document
)
from .serializers import (
    DocumentSerializer
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


@api_view(['GET'])
def all_documents(request):
    doc_objs = Document.objects.all()
    serializer = DocumentSerializer(doc_objs, many=True)
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

@api_view(['POST'])
def add_text(request):
    """
    API endpoint for adding a piece of text
    """
    body = json.loads(request.body.decode('utf-8'))
    new_text_obj = Document()
    new_text_obj.save()
    Document.update_metadata(body)
    serializer = DocumentSerializer(new_text_obj)
    return Response(serializer.data)

