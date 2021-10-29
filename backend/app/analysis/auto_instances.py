from app.models import Document, Corpus
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
                doc_title = doc.replace(".txt", "")
                if Document.objects.filter(title=doc_title).count() == 0:   #If the doc isn't already an instance in the Document model:
                    new_doc = Document.objects.create_document(title=doc_title, text=line)
                    new_doc.save()
                #print(new_doc.title)
                #print(f"{docList[-1].title}: {docList[-1].text}")

    #return Documents.objects.all()

def main():
    create_instances_new()
    #print("sup")
    #print(len(Document.objects.all()))
    #for doc in Document.objects.all():
        #print("bup")
        #print(f"{doc.title}: {doc.tokenized_text}")
    #print("nup")
    #print(unmanaged_docs[0].title)
    #print(unmanaged_docs[0].tokenized_text)
    if Corpus.objects.filter(title="Small Talks Corpus").count() == 0:
        tt_corpus = Corpus(title="Small Talks Corpus")
        tt_corpus.save()
    else:
        tt_corpus = Corpus.objects.filter(title="Small Talks Corpus")[0]

    tt_corpus.documents.set(Document.objects.all())
    tt_corpus.save()
    print(Corpus.objects.all())
    print("Documents: ")
    for doc in tt_corpus:
        print(doc.title)