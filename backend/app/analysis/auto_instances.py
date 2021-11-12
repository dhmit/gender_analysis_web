from app.models import Document, Corpus
import os
import csv
from app.services.parse_csv import parse_csv

def create_instances():
    directory = "C:\\Users\\Ayden\\Documents\\GitHub\\gender_analysis_web\\backend\\app\\analysis\\small_talks"
    # Make the line above shorter at some point
    documents = os.listdir(directory)
    print(documents)
    docList = []
    for doc in documents:
        with open(f"{directory}\\{doc}") as newDoc:
            for line in newDoc:
                docList.append(Document(title=doc.replace(".txt", ""), text=line))
                #print(f"{docList[-1].title}: {docList[-1].text}")

    return docList

def create_instances_new():
    directory = "C:\\Users\\Ayden\\Documents\\GitHub\\gender_analysis_web\\backend\\app\\analysis\\small_talks"
    # Make the line above shorter at some point
    documents = os.listdir(directory)

    for doc in documents:
        with open(f"{directory}\\{doc}") as newDoc:
            for line in newDoc:
                doc_title = doc.replace(".txt", "")
                if Document.objects.filter(title=doc_title).count() == 0:   #If the doc isn't already an instance in the Document model:
                    new_doc = Document.objects.create_document(title=doc_title, text=line)
                    new_doc.save()
                #print(new_doc.title)
                #print(f"{docList[-1].title}: {docList[-1].text}")

    #return Documents.objects.all()

def create_instances_newer(csv_filename):
    current_path = os.path.dirname(os.path.abspath(__file__))  # returns path of auto_instances.py
    in_csv = os.path.join(current_path, csv_filename)  # appends small_talks.csv to the above

    with open(in_csv, encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        return parse_csv(csv_reader, csv_filename)

def main():
    create_instances_newer("small_talks.csv")