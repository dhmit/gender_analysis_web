"""
Miscellaneous utility functions and variables useful throughout the system
"""
from textwrap import dedent
from nltk.corpus import stopwords

SWORDS_ENG = stopwords.words('english')

NLTK_TAGS = {
    'CC': 'conjunction, coordinating',
    'CD': 'numeral, cardinal',
    'DT': 'determiner',
    'EX': 'existential there',
    'IN': 'preposition or conjunction, subordinating',
    'JJ': 'adjective or numeral, ordinal',
    'JJR': 'adjective, comparative',
    'JJS': 'adjective, superlative',
    'LS': 'list item marker',
    'MD': 'modal auxiliary',
    'NN': 'noun, common, singular or mass',
    'NNP': 'noun, proper, singular',
    'NNS': 'noun, common, plural',
    'PDT': 'pre-determiner',
    'POS': 'genitive marker',
    'PRP': 'pronoun, personal',
    'PRP$': 'pronoun, possessive',
    'RB': 'adverb',
    'RBR': 'adverb, comparative',
    'RBS': 'adverb, superlative',
    'RP': 'particle',
    'TO': '"to" as preposition or infinitive marker',
    'UH': 'interjection',
    'VB': 'verb, base form',
    'VBD': 'verb, past tense',
    'VBG': 'verb, present participle or gerund',
    'VBN': 'verb, past participle',
    'VBP': 'verb, present tense, not 3rd person singular',
    'VBZ': 'verb, present tense, 3rd person singular',
    'WDT': 'WH-determiner',
    'WP': 'WH-pronoun',
    'WRB': 'Wh-adverb',
}

def compute_bin_year(year, time_frame_start, bin_size):
    """
    Given an input year, the start of a time frame, and bin size,
    computes which bin start date this year belongs to.
    """
    return ((year - time_frame_start) // bin_size) * bin_size + time_frame_start