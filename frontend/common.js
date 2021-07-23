/**
 * Common.js -- miscellaneous routines useful throughout the system
 */


export const NLTK_TAGS = {
    "CC": "conjunction, coordinating",
    "CD": "numeral, cardinal",
    "DT": "determiner",
    "EX": "existential there",
    "IN": "preposition or conjunction, subordinating",
    "JJ": "adjective or numeral, ordinal",
    "JJR": "adjective, comparative",
    "JJS": "adjective, superlative",
    "LS": "list item marker",
    "MD": "modal auxiliary",
    "NN": "noun, common, singular or mass",
    "NNP": "noun, proper, singular",
    "NNS": "noun, common, plural",
    "PDT": "pre-determiner",
    "POS": "genitive marker",
    "PRP": "pronoun, personal",
    "PRP$": "pronoun, possessive",
    "RB": "adverb",
    "RBR": "adverb, comparative",
    "RBS": "adverb, superlative",
    "RP": "particle",
    "TO": "\"to\" as preposition or infinitive marker",
    "UH": "interjection",
    "VB": "verb, base form",
    "VBD": "verb, past tense",
    "VBG": "verb, present participle or gerund",
    "VBN": "verb, past participle",
    "VBP": "verb, present tense, not 3rd person singular",
    "VBZ": "verb, present tense, 3rd person singular",
    "WDT": "WH-determiner",
    "WP": "WH-pronoun",
    "WRB": "Wh-adverb"
};

export const PRONOUN_TYPES = {
    "subj": "Subject",
    "obj": "Object",
    "pos_det": "Possessive determiner",
    "pos_pro": "Possessive pronoun",
    "reflex": "Reflexive"
};


/**
 * Get the value of a cookie, given its name
 * Adapted from https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
 * @param {string} name - The name of the cookie
 */
export function getCookie(name) {
    let cookieValue;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (const rawCookie of cookies) {
            const cookie = rawCookie.trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

