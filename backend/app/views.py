"""
These view functions and classes implement API endpoints
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from .models import ()
# from .serializers import ()

@api_view(['GET'])
def example(request, example_id):
    """
    API example endpoint.
    """
    data = {
        'name': 'Example',
        'id': example_id,
    }
    return Response(data)
