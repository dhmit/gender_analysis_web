

import csv
from app.services import parse_csv


@api_view(['POST'])
def upload_doc(request):
    """
    API endpoint for uploading csv files that are to be converted to an instance of csv_reader
    """
    file=request.data
    #inserts if condition?(to check whether input data is csv)
    csv_reader = csv.DictReader(file)
    x= parse_csv(csv_reader)#returns None because parse_csv doesn't return anything
    return x


