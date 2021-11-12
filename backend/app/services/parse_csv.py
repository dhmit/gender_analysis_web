from app.models import Document, Corpus

def parse_csv(csv_reader, title):
    doc_list = []
    for data in csv_reader:
        new_doc = None
        if Document.objects.filter(title=data['title']).count() == 0:  # If the data isn't already an instance in the Document model:
            new_doc = Document.objects.create_document(title=data['title'], text=data['transcript'], author=data['speaker_1'], year=data['recorded_date'][:4])
            new_doc.save()
        else:
            new_doc = Document.objects.filter(title=data['title'])[0]
        doc_list.append(new_doc)

    # Use the id as a unique indentifier instead of the title (or maybe remove this check entirely)
    if Corpus.objects.filter(title=f"{title} Corpus").count() == 0:  # If the corpus doesn't exist...
        new_corpus = Corpus(title=f"{title} Corpus")
        new_corpus.save()
    else:
        new_corpus = Corpus.objects.filter(title=f"{title} Corpus")[0]

    new_corpus.documents.set(doc_list)
    new_corpus.save()
    print(Corpus.objects.all())
    print("Documents: ")
    for doc in new_corpus:
        print(doc.title)

    return new_corpus