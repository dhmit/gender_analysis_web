"""
Miscellaneous utility functions and variables useful throughout the system
"""
from textwrap import dedent
from nltk.corpus import stopwords

FEMALE_HONORIFICS = ["Miss", "Mrs", "Mrs.", "Ms", "Mistress", "Madam", "Ma'am", "Dame",
                     "Lady", "Her Honour", "Her Honor", "My Lady", "Your Ladyship",
                     "Sr", "Sister", "Sayyidah"]
MALE_HONORIFICS = ["Master", "Mr", "Mr.", "Mr .", "Sir", "Gentleman", "Sire", "Lord", "His Honour",
                   "His Honor", "My Lord", "Your Lordship", "Master", "Esquire", "Esq",
                   "His Holiness", "Pope", "His All Holiness", "His Beatitude", "The Reverend",
                   "Rev", "Fr", "Father", "Pr", "Pastor", "Br", "Brother", "Rabbi", "Imam",
                   "Mufti", "Sayyid", "Captain"]
NEUTRAL_HONORIFICS = ["Mx", "Excellency", "Excellence", "Your Honor", "The Honorable",
                      "The Honourable", "The Hon", "Hon", "The Hon'ble", "The Right Honourable",
                      "The Most Honourable", "Dr", "Doctor", "Professor", "QC", "Cl", "S Cl",
                      "Counsel", "Senior Counsel", "Eur Ing", "Vice-Chancellor", "Principal",
                      "President", "Warden", "Dean", "Regent", "Rector", "Provost", "Director",
                      "Chief Executive", "Venerable", "Eminent"]
HONORIFICS = FEMALE_HONORIFICS + MALE_HONORIFICS + NEUTRAL_HONORIFICS

# Common Pronoun Collections
HE_SERIES =  ['he', 'his', 'him', 'himself']
SHE_SERIES = ['she', 'her', 'hers', 'herself']
THEY_SERIES = ['they', 'them', 'theirs', 'themself']
IT_SERIES = ['it', 'itself']
XE_SERIES = ['xe', 'xem', 'xyr', 'xyrs', 'xemself']
AE_SERIES = ['ae', 'aer', 'aers', 'aerself']
FAE_SERIES = ['fae', 'faer', 'faers', 'faerself']
EY_SERIES = ['ey', 'em', 'eir', 'eirs', 'eirself']
VE_SERIES = ['ve', 'ver', 'vis', 'verself']
PER_SERIES = ['per', 'pers', 'perself']
ZE_HIR_SERIES = ['ze', 'hir', 'hirs', 'hirself']
USER_DEFINED_SERIES = []

PRONOUN_COLLECTIONS = [HE_SERIES, SHE_SERIES, THEY_SERIES, IT_SERIES, XE_SERIES, AE_SERIES, FAE_SERIES, EY_SERIES, VE_SERIES, PER_SERIES, ZE_HIR_SERIES, USER_DEFINED_SERIES]

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

NLTK_TAGS_ADJECTIVES = ["JJ", "JJR", "JJS"]


def print_header(header_str):
    """
    Print a header -- mostly for our command line tools.
    """
    print(dedent(f'''
        ################################################################################
        # {header_str}
        ################################################################################'''))
