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
                docList.append(Document(title=doc, text=line))
                print(f"{docList[-1].title}: {docList[-1].text}")