"""
Miscellaneous utility functions useful throughout the system
"""
from textwrap import dedent

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


def print_header(header_str):
    """
    Print a header -- mostly for our command line tools.
    """
    print(dedent(f'''
        ################################################################################
        # {header_str}
        ################################################################################'''))
