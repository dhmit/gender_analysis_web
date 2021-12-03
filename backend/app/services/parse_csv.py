from app.models import Document, Corpus

def parse_csv(csv_reader, title="new_data"):
    doc_list = []
    for data in csv_reader:
        new_doc = None
        new_doc = Document.objects.create_document(title=data['title'], text=data['transcript'], author=data['speaker_1'], year=data['recorded_date'][:4])
        # The line above creates a new Document instance (You should probably find some way of getting the user to assign columns to keys.For now, assume these keys match whatever dataset we're using.)
        new_doc.save()
        doc_list.append(new_doc)

    new_corpus = Corpus(title=f"{title} Corpus")
    new_corpus.save()

    new_corpus.documents.set(doc_list)
    new_corpus.save()

    return new_corpus