from app.models import Document, Corpus

def parse_csv(csv_reader):
    doc_list = []
    for data in csv_reader:
        new_doc = None
        if Document.objects.filter(title=data['title']).count() == 0:  # If the data isn't already an instance in the Document model:
            new_doc = Document.objects.create_document(title=data['title'], text=data['transcript'], author=data['speaker_1'], year=data['recorded_date'][:4])
            new_doc.save()
        else:
            new_doc = Document.objects.filter(title=data['title'])[0]
        doc_list.append(new_doc)

    #Standardize title
    if Corpus.objects.filter(title="Small Talks Corpus").count() == 0:  #If the corpus doesn't exist...
        tt_corpus = Corpus(title="Small Talks Corpus")
        tt_corpus.save()
    else:
        tt_corpus = Corpus.objects.filter(title="Small Talks Corpus")[0]

    tt_corpus.documents.set(doc_list)
    tt_corpus.save()
    print(Corpus.objects.all())
    print("Documents: ")
    for doc in tt_corpus:
        print(doc.title)