# Gender Analysis Web

This project is an extension of the work originally begun in https://github.com/dhmit/gender_analysis.

## A note on the neuralcoref package

This project uses the Python package [neuralcoref](https://pypi.org/project/neuralcoref/), 
which requires a few extra steps to install. Note that the following instructions
are meant for those set up with the DHMIT lab's tooling 
(for which see [here](https://urop.dhmit.xyz)).

To install, follow the following steps:
- Open requirements.txt in PyCharm, click the 'Install requirements' button. This will clone the package directly 
  into your `venv/src` directory and may take a while. If you're working in PyCharm, 
  this will ultimately produce an error ("Installing packages failed.") This is expected.
- In the PyCharm terminal, run `pip install -r venv/src/neuralcoref/requirements.txt`.
- In the PyCharm terminal, run `pip install -e venv/src/neuralcoref`.
- In the PyCharm terminal, run `python -m spacy download en_core_web_sm`.

To test out the package, you can open up your Python console and run the following commands:
```
>>> import spacy
>>> import neuralcoref
>>> nlp = spacy.load('en_core_web_sm')
>>> neuralcoref.add_to_pipe(nlp)
>>> doc = nlp(u'My sister has a dog. She loves him.')
>>> doc._.coref_clusters
[My sister: [My sister, She], a dog: [a dog, him]]
```

Documentation for this package can be found [here](https://github.com/huggingface/neuralcoref).