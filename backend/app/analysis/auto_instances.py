from app.models import Document
import os

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
                new_doc = Document.objects.create_document(title=doc.replace(".txt", ""), text=line)
                #print(new_doc.title)
                #print(f"{docList[-1].title}: {docList[-1].text}")

    #return Documents.objects.all()

def main():
    create_instances_new()
    for doc in Document.objects.all():
        print(f"{doc.title}: {doc.tokenized_text}")
    #print(unmanaged_docs[0].title)
    #print(unmanaged_docs[0].tokenized_text)