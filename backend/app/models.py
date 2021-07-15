"""
Models for the gender analysis web app.
"""
import nltk
import string
import re
from collections import Counter
from more_itertools import windowed
from django.db import models
from .fields import LowercaseCharField
from .managers import DocumentManager, AliasManager, CharacterManager
from .common import HONORIFICS, PRONOUN_COLLECTIONS
from .analysis.ner import filter_honr

import neuralcoref
import spacy

nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp)


class PronounSeries(models.Model):
    """
    A class that allows users to define a custom series of pronouns to be used in
    analysis functions
    """

    # Things to consider:
    # Add a default to reflex? i.e. default = object pronoun + 'self'?
    # Also, how to we run doctests here? Or use pytest? (configs don't recognize django package or relative filepath
    # in import statement)
    identifier = models.CharField(max_length=60)
    subj = LowercaseCharField(max_length=40)
    obj = LowercaseCharField(max_length=40)
    pos_det = LowercaseCharField(max_length=40)
    pos_pro = LowercaseCharField(max_length=40)
    reflex = LowercaseCharField(max_length=40)

    @property
    def all_pronouns(self):
        """
        :return: The set of all pronoun identifiers.
        """
        pronoun_set = {
            self.subj,
            self.obj,
            self.pos_det,
            self.pos_pro,
            self.reflex,
        }

        return pronoun_set

    def __contains__(self, pronoun):
        """
        Checks to see if the given pronoun exists in this group. This check is case-insensitive
        >>> pronouns = ['They', 'Them', 'Their', 'Theirs', 'Themself']
        >>> pronoun_group = PronounSeries.objects.create('Andy', *pronouns)
        >>> 'they' in pronoun_group
        True
        >>> 'hers' in pronoun_group
        False
        :param pronoun: The pronoun to check for in this group
        :return: True if the pronoun is in the group, False otherwise
        """

        return pronoun.lower() in self.all_pronouns

    def __iter__(self):
        """
        Allows the user to iterate over all of the pronouns in this group. Pronouns
        are returned in lowercase and order is not guaranteed.
        >>> pronouns = ['she', 'her', 'her', 'hers', 'herself']
        >>> pronoun_group = PronounSeries.objects.create('Fem', *pronouns)
        >>> sorted(pronoun_group)
        ['her', 'hers', 'herself', 'she']
        """

        yield from self.all_pronouns

    def __repr__(self):
        """
        >>> PronounSeries.objects.create(
        ...     identifier='Masc',
        ...     subj='he',
        ...     obj='him',
        ...     pos_det='his',
        ...     pos_pro='his',
        ...     reflex='himself'
        ... )
        <Masc: ['he', 'him', 'himself', 'his']>
        :return: A console-friendly representation of the pronoun series
        """

        return f'<{self.identifier}: {list(sorted(self))}>'

    def __str__(self):
        """
        >>> str(PronounSeries.objects.create('Andy', *['Xe', 'Xem', 'Xis', 'Xis', 'Xemself']))
        'Andy-series'
        :return: A string-representation of the pronoun series
        """

        return self.identifier + '-series'

    def __hash__(self):
        """
        Makes the `PronounSeries` class hashable
        """

        return self.identifier.__hash__()

    def __eq__(self, other):
        """
        Determines whether two `PronounSeries` are equal. Note that they are only equal if
        they have the same identifier and the exact same set of pronouns.

        >>> fem_series = PronounSeries.objects.create(
        ...     identifier='Fem',
        ...     subj='she',
        ...     obj='her',
        ...     pos_det='her',
        ...     pos_pro='hers',
        ...     reflex='herself'
        ... )
        >>> second_fem_series = PronounSeries.objects.create(
        ...     identifier='Fem',
        ...     subj='she',
        ...     obj='her',
        ...     pos_pro='hers',
        ...     reflex='herself'
        ...     pos_det='HER',
        ... )
        >>> fem_series == second_fem_series
        True
        >>> masc_series = PronounSeries.objects.create(
        ...     identifier='Masc',
        ...     subj='he',
        ...     obj='him',
        ...     pos_det='his',
        ...     pos_pro='his',
        ...     reflex='himself'
        ... )
        >>> fem_series == masc_series
        False
        :param other: The `PronounSeries` object to compare
        :return: `True` if the two series are the same, `False` otherwise.
        """

        return (
                self.identifier == other.identifier
                and sorted(self) == sorted(other)
        )


class Gender(models.Model):
    """
    This model defines a gender that analysis functions will use to operate.
    """

    label = models.CharField(max_length=60)
    pronoun_series = models.ManyToManyField(PronounSeries)

    def __repr__(self):
        """
        :return: A console-friendly representation of the gender
        >>> Gender('Female')
        <Female>
        """

        return f'<{self.label}>'

    def __str__(self):
        """
        :return: A string representation of the gender
        >>> str(Gender('Female')
        'Female'
        """

        return self.label

    def __hash__(self):
        """
        Allows the Gender object to be hashed
        """

        return self.label.__hash__()

    def __eq__(self, other):
        """
        Performs a check to see whether two `Gender` objects are equivalent. This is true if and
        only if the `Gender` identifiers, pronoun series, and names are identical.

        Note that this comparison works:
        >>> fem_pronouns = PronounSeries.objects.create('Fem', *['she', 'her', 'her', 'hers', 'herself'])

        >>> female = Gender.objects.create('Female')
        >>> female.pronoun_series.add(1)

        >>> another_female = Gender.objects.create('Female')
        >>> another_female.pronoun_series.add(1)

        >>> female == another_female
        True

        But this one does not:
        >>> they_series = PronounSeries.objects.create('They', *['they', 'them', 'their', 'theirs', 'themselves'])
        >>> xe_series = PronounSeries.objects.create('They', *['Xe', 'Xem', 'Xis', 'Xis', 'Xemself'])

        >>> androgynous_1 = Gender.objects.create('NB')
        >>> androgynous_1.pronoun_series.add(2)

        >>> androgynous_2 = Gender.objects.create('NB')
        >>> androgynous_2.pronoun_series.add(3)

        >>> androgynous_1 == androgynous_2
        False
        :param other: The other `Gender` object to compare
        :return: `True` if the `Gender`s are the same, `False` otherwise
        """

        return (
                self.label == other.label
                and list(self.pronoun_series.all()) == list(other.pronoun_series.all())
        )

    @property
    def pronouns(self):
        """
        :return: A set containing all pronouns that this `Gender` uses
        >>> they_series = PronounSeries.objects.create('They', *['they', 'them', 'their', 'theirs', 'themselves'])
        >>> xe_series = PronounSeries('Xe', *['Xe', 'Xer', 'Xis', 'Xis', 'Xerself'])
        >>> androgynous = Gender.objects.create('Androgynous')
        >>> androgynous.pronoun_series.add(1, 2)
        >>> androgynous.pronouns == {'they', 'them', 'theirs', 'xe', 'xer', 'xis'}
        True
        """

        all_pronouns = set()
        for series in list(self.pronoun_series.all()):
            all_pronouns |= series.all_pronouns

        return all_pronouns

    @property
    def subj(self):
        """
        :return: set of all subject pronouns used to describe the gender
        >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> masc_pronouns = PronounSeries('Masc', {'he', 'him', 'his'}, subj='he', obj='him')
        >>> bigender = Gender('Bigender', [fem_pronouns, masc_pronouns])
        >>> bigender.subj == {'he', 'she'}
        True
        """

        subject_pronouns = set()
        for series in list(self.pronoun_series.all()):
            subject_pronouns.add(series.subj)

        return subject_pronouns

    @property
    def obj(self):
        """
        :return: set of all object pronouns used to describe the gender
        >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> masc_pronouns = PronounSeries('Masc', {'he', 'him', 'his'}, subj='he', obj='him')
        >>> bigender = Gender('Bigender', [fem_pronouns, masc_pronouns])
        >>> bigender.obj == {'him', 'her'}
        True
        """

        subject_pronouns = set()
        for series in list(self.pronoun_series.all()):
            subject_pronouns.add(series.obj)
        return subject_pronouns


class Alias(models.Model):
    """
    An Alias object is one name along with its associated metadata: mentions,
    coref clusters, and so forth. A Character object is made up of aliases.
    """

    name = models.CharField(max_length=255, blank=True)
    count = models.IntegerField(null=True, blank=True)
    mentions = models.JSONField(null=True, blank=True, default=list)
    coref_clusters = models.JSONField(null=True, blank=True, default=list)
    raw_pronouns = models.JSONField(null=True, blank=True, default=list)
    pronoun_rates = models.JSONField(null=True, blank=True, default=list)
    sanitized_pronoun_rates = models.JSONField(null=True, blank=True, default=list)

    objects = AliasManager()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def set_coref_clusters(self, coref_clusters):
        self.coref_clusters = coref_clusters

    def set_mentions(self, mentions):
        self.mentions = mentions

    def get_mentions(self):
        return self.mentions

    def get_coref_clusters(self):
        return self.coref_clusters

    def get_name(self):
        return self.name

    def get_count(self):
        return self.count

    def calculate_pronouns(self):

        raw_pronoun_dict = {}

        overall_pronoun_count = 0

        raw_pronoun_dict = {p[0]: 0 for p in PRONOUN_COLLECTIONS if p}

        for clu in self.coref_clusters:
            mention_list = clu['mentions']
            for mention in mention_list:
                for pronoun_group in PRONOUN_COLLECTIONS:
                    if mention in pronoun_group:
                        overall_pronoun_count += 1
                        raw_pronoun_dict[pronoun_group[0]] += 1

        # calculate pronoun_rate
        pronoun_rates = {}
        for pronoun in raw_pronoun_dict.keys():
            if raw_pronoun_dict[pronoun]:
                percentage = round(raw_pronoun_dict[pronoun] / overall_pronoun_count, 3)
            else:
                percentage = 0.00

            pronoun_rates[pronoun] = percentage

        # sanitize and get rid of the 0.00 result
        sanitized_pronouns = {}

        for pro in pronoun_rates.keys():
            if pronoun_rates[pro]:
                sanitized_pronouns[pro] = pronoun_rates[pro]
        if not pronoun_rates:
            sanitized_pronouns = {'unknown': 1.0}

        return raw_pronoun_dict, pronoun_rates, sanitized_pronouns


class Character(models.Model):
    """
    A Character object is a collection of information about a person-entity.
    Mostly it's a collection of aliases, with rolled up metadata for the sake of
    convenience and display.


    We initialize with any alias.
    """
    aliases = models.ManyToManyField(Alias)

    common_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    honorifics = models.JSONField(null=True, blank=True, default=list)
    main_title = models.CharField(max_length=255, blank=True)

    gender = models.JSONField(null=True, blank=True, default=dict)

    count = models.IntegerField(null=True, blank=True)

    mentions = models.JSONField(null=True, blank=True, default=list)
    coref_clusters = models.JSONField(null=True, blank=True, default=list)

    objects = CharacterManager()

    def __repr__(self):
        return self.common_name

    def display(self):
        print("~~~~~~~~~~")
        print("Common Name:", self.common_name)
        """
        debugging
        print(". Honorific:", self.main_title)
        print(". First Name:", self.first_name)
        print(". Middle Name:", self.middle_name)
        print(". Last Name:", self.last_name)
        """
        print("Full Name:", self.full_name)
        print("Total Count:", self.count)
        print("Alias Makeup:",
              [(alias.get_name(), (str(round((alias.count / self.count) * 100, 2)) + "%")) for alias in
               list(self.aliases.all())])
        print("Gender Probabilities:", self.gender)

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_common_name(self):
        return self.common_name

    def guess_full_name(self):
        # Take all the info we have and do a best guess at title, first name,
        # middle names, and last name.

        honorifics_and_counts = []
        firstname_candidates = []
        middlename_candidates = []
        lastname_candidates = []
        names = []

        split_common_name = self.get_common_name().split(" ")
        # Separate out honorifics and other words, which we presume are names.
        # Keep them in tuples with how often they occur.

        for alias in list(self.aliases.all()):
            name = alias.get_name()
            names.append(name)
            words = name.split(" ")

            likelihood = .5
            if len(words) == 1:
                if words[0] in HONORIFICS or words[0][:-1] in HONORIFICS:
                    honorifics_and_counts.append((words[0], alias.get_count()))
                else:
                    firstname_candidates.append((words[0], likelihood))
                    lastname_candidates.append((words[0], likelihood))

            elif len(words) == 2:
                if words[0] in HONORIFICS or words[0][:-1] in HONORIFICS:
                    honorifics_and_counts.append((words[0], alias.get_count()))
                    if words[1] in split_common_name:
                        likelihood += .05
                    firstname_candidates.append((words[1], likelihood))
                    lastname_candidates.append((words[1], likelihood))
                else:
                    for x in range(len(words)):
                        word_likelihood = .6
                        if words[x] in split_common_name:
                            word_likelihood += .05
                        if x == 0:
                            firstname_candidates.append((words[0], word_likelihood))
                        elif x == 1:
                            lastname_candidates.append((words[1], word_likelihood))

            elif len(words) == 3:
                if words[0] in HONORIFICS or words[0][:-1] in HONORIFICS:
                    honorifics_and_counts.append((words[0], alias.get_count()))
                    for x in range(1, len(words)):
                        word_likelihood = .7
                        if words[x] in split_common_name:
                            word_likelihood += .05
                        if x == 0:
                            firstname_candidates.append((words[1], word_likelihood))
                        elif x == 1:
                            lastname_candidates.append((words[2], word_likelihood))
                else:
                    for x in range(len(words)):
                        word_likelihood = .8
                        if words[x] in split_common_name:
                            word_likelihood += .05
                        if x == 0:
                            firstname_candidates.append((words[0], word_likelihood))
                        elif x == 1:
                            middlename_candidates.append((words[1], word_likelihood))
                        elif x == 2:
                            lastname_candidates.append((words[2], word_likelihood))

            elif len(words) == 4:
                if words[0] in HONORIFICS or words[0][:-1] in HONORIFICS:
                    honorifics_and_counts.append((words[0], alias.get_count()))
                    for x in range(1, len(words)):
                        word_likelihood = .9
                        if words[x] in split_common_name:
                            word_likelihood += .05
                        if x == 0:
                            firstname_candidates.append((words[1], word_likelihood))
                        elif x == 1:
                            middlename_candidates.append((words[2], word_likelihood))
                        elif x == 2:
                            lastname_candidates.append((words[3], word_likelihood))

        truename_guess = []
        real_truename_guess = []

        if honorifics_and_counts:
            most_common_title = honorifics_and_counts[0][0]
            self.main_title = most_common_title
            real_truename_guess.append(most_common_title)

        if firstname_candidates:
            best_firstname_guess = (sorted(firstname_candidates, key=lambda x: x[1], reverse=True))[0]
            truename_guess.append(best_firstname_guess)
            self.first_name = best_firstname_guess[0]

        if middlename_candidates:
            best_middlename_guess = (sorted(middlename_candidates, key=lambda x: x[1], reverse=True))[0]
            truename_guess.append(best_middlename_guess)
            self.middle_name = best_middlename_guess[0]

        if lastname_candidates:
            best_lastname_guess = sorted(lastname_candidates, key=lambda x: x[1], reverse=True)[0]
            truename_guess.append(best_lastname_guess)
            self.lastname = best_lastname_guess[0]

        for word in truename_guess:
            if word[0] not in real_truename_guess:
                real_truename_guess.append(word[0])
        real_truename_guess = " ".join(real_truename_guess)

        return real_truename_guess

    def guess_gender(self):
        # Use neuralcoref clusters to get pronouns used for the character,
        # then set 'gender' to the most likely gender and 'gender_probability'
        # to a list of all nonzero pronouns, ranked, with % of frequency

        raw_pronoun_dict = {}
        raw_pronoun_dict = {p[0]: 0 for p in PRONOUN_COLLECTIONS if p}
        overall_pronoun_count = 0

        for pronoun in raw_pronoun_dict.keys():
            for alias in list(self.aliases.all()):
                raw_alias_pronouns = alias.raw_pronouns
                if pronoun in raw_alias_pronouns.keys():
                    raw_pronoun_dict[pronoun] += raw_alias_pronouns[pronoun]
                    overall_pronoun_count += raw_alias_pronouns[pronoun]

        # calculate pronoun_rate
        pronoun_rates = {}
        for pronoun in raw_pronoun_dict.keys():
            if raw_pronoun_dict[pronoun]:
                percentage = round(raw_pronoun_dict[pronoun] / overall_pronoun_count, 3)
            else:
                percentage = 0.00

            pronoun_rates[pronoun] = percentage

        # sanitize and get rid of the 0.00 result
        sanitized_pronouns = {}

        for pro in pronoun_rates.keys():
            if pronoun_rates[pro]:
                sanitized_pronouns[pro] = round(pronoun_rates[pro] * 100, 2)

        if not sanitized_pronouns:
            sanitized_pronouns = {'unknown': 100}

        sanitized_pronouns_sorted = sorted(sanitized_pronouns.items(), key=lambda item: item[1], reverse=True)
        return sanitized_pronouns_sorted

    def collate_mentions(self):
        all_mentions = []

        for alias in list(self.aliases.all()):
            all_mentions.extend(alias.get_mentions())

        return all_mentions

    def collate_coref_clusters(self):
        all_coref_clusters = []

        for alias in list(self.aliases.all()):
            all_coref_clusters.extend(alias.get_coref_clusters())

        return all_coref_clusters

    def update_character(self):
        """
        Use this function whenever adding or removing an alias to update the
        Character object's metadata.
        """

        self.mentions = self.collate_mentions()
        self.coref_clusters = self.collate_coref_clusters()
        self.gender = self.guess_gender()
        self.full_name = self.guess_full_name()
        self.count = sum([alias.count for alias in list(self.aliases.all())])
        self.save()

    def add_alias(self, alias):
        # (Mostly) reversable function that nondestructibly
        # merges a character into another character.

        if alias.name in list(self.aliases.all()):
            print("Cannot merge", alias.name, "with", self.common_name, "because they're already here!")
            return False

        elif alias.count > self.count:
            print(alias.name, "is more common than", self.common_name, ". Updating common_name to", alias.name)
            self.common_name = alias.get_name()
            self.count = alias.get_count()

        self.aliases.add(alias)

        self.update_character()

    def remove_alias(self, alias_common_name):
        # Removes an alias by common name from association with the character. Returns the removed
        # alias, in case we want to do something with it.

        if alias_common_name not in [alias.name for alias in self.aliases]:
            print("Cannot remove", alias_common_name, "because it isn't a part of", self.common_name)
            return False
        elif alias_common_name == self.common_name:
            print("Cannot remove", alias_common_name, "because it is this character's common name.")
            return False

        alias = next((alias for alias in self.aliases if alias.name == alias_common_name), None)
        self.aliases.remove(alias)
        self.update_character()
        print("Removed", alias_common_name, "from", self.common_name, ".")
        return alias


class Document(models.Model):
    """
    This model will hold the full text and
    metadata (author, title, publication date, etc.) of a document
    """
    author = models.CharField(max_length=255, blank=True)
    year = models.IntegerField(null=True, blank=True)
    new_attributes = models.JSONField(null=True, blank=True, default=dict)
    text = models.TextField(blank=True)
    title = models.CharField(max_length=255, blank=True)
    word_count = models.PositiveIntegerField(blank=True, null=True, default=None)
    tokenized_text = models.JSONField(null=True, blank=True, default=None)
    word_count_counter = models.JSONField(null=True, blank=True, default=dict)
    part_of_speech_tags = models.JSONField(null=True, blank=True, default=list)

    sentences = models.JSONField(null=True, blank=True, default=list)
    sentence_tokens = models.JSONField(null=True, blank=True, default=list)
    sentence_pos_tags = models.JSONField(null=True, blank=True, default=list)
    sentence_chunks = models.JSONField(null=True, blank=True, default=list)


    name_list = models.JSONField(null=True, blank=True, default=list)
    name_dict = models.JSONField(null=True, blank=True, default=dict)
    name_coref_dict = models.JSONField(null=True, blank=True, default=dict)

    aliases = models.ManyToManyField(Alias)
    characters = models.ManyToManyField(Character)

    objects = DocumentManager()

    def _clean_quotes(self):
        """
        Scans through the text and replaces all of the smart quotes and apostrophes with their
        "normal" ASCII variants

        :param self: The Document to reformat
        :return: A string that is identical to `text`, except with its smart quotes exchanged
        """
        self.text = re.sub(r'[\“\”]', '\"', re.sub(r'[\‘\’]', '\'', self.text))
        self.save()
        return self.text

    def get_tokenized_text_wc_and_pos(self):
        """
        Tokenizes the text of a Document and returns it as a list of tokens, while removing all punctuation
        and converting everything to lowercase.

        :param self: The Document to tokenize
        :return: none
        """
        self._clean_quotes()
        tokens = nltk.word_tokenize(self.text)
        excluded_characters = set(string.punctuation)
        tokenized_text = [word.lower() for word in tokens if word not in excluded_characters]
        self.tokenized_text = tokenized_text
        self.word_count = len(self.tokenized_text)
        self.word_count_counter = Counter(self.tokenized_text)
        self.part_of_speech_tags = nltk.pos_tag(self.tokenized_text)
        self.save()

    def get_tokenized_sentences(self):
        """
        Gets all of the different tokens we need to perform NER analysis on a document.
        Uses the raw text, not the cleaned text. It may be that we don't actually need to store all of
        these; we can catch that on a refactor.

        :param self: the document to tokenize
        :return: none
        """

        text = self.text
        sentences = nltk.sent_tokenize(text)

        sentence_tokens = []
        sentence_pos_tags = []
        sentence_chunks = []

        for sent in sentences:
            tokens = nltk.word_tokenize(sent)
            sentence_tokens.append(tokens)

            pos_tags = nltk.pos_tag(tokens)
            sentence_pos_tags.append(pos_tags)

            chunks = nltk.ne_chunk(pos_tags)
            sentence_chunks.append(chunks)

        self.sentences = sentences
        self.sentence_tokens = sentence_tokens
        self.sentence_pos_tags = sentence_pos_tags
        self.sentence_chunks = sentence_chunks

        self.save()

    def get_name_list(self):
        """
        Checks to see if we've done sentence-level tokenization, and then identifies all PERSONS in the text.

        :param self: the document to get the character list for.
        returns a sorted list of character names.
        """

        labels_char = []
        labels = 'FACILITY,GPE,GSP,LOCATION,ORGANIZATION,PERSON'

        if not self.sentences:
            self.get_tokenized_sentences()

        char_dict = {lab: {} for lab in labels.split(',')}

        for x in range(len(self.sentences)):
            for y in range(len(self.sentence_chunks[x])):
                chunk = self.sentence_chunks[x][y]
                if isinstance(chunk, nltk.tree.Tree):
                    output = ' '.join(c[0] for c in chunk)
                    # This ugly code checks to see if the potential entity is preceded by a "Mrs." or a "Ms."
                    # It patches an error whereby NLTK's chunker doesn't think married women are persons.
                    if y != 0:
                        previous_chunk = self.sentence_chunks[x][y - 1][0]
                        if not isinstance(previous_chunk, nltk.tree.Tree) and not isinstance(previous_chunk, tuple):
                            if previous_chunk.lower() == "mrs." or previous_chunk.lower() == "mrs":
                                output = previous_chunk + " " + ' '.join(c[0] for c in chunk)
                        labels_char.append((chunk.label(), output))
                    else:
                        labels_char.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        for character in labels_char:
            label, name = character
            char_dict[label][name] = char_dict[label].get(name, 0) + 1

        people = char_dict['PERSON']
        name_list = [(p, people[p]) for p in people if p not in HONORIFICS and p[:-1] not in HONORIFICS]

        self.name_list = sorted(name_list, key=lambda p: p[1], reverse=True)
        self.save()
        return self.name_list

    def get_mentions_full_charlist(self):
        """
        Given a list of names, this function goes through and finds every
        sentence in which the character name appears within the provided text.

        It returns a dictionary in the form dict[name] = [index_of_sentence_1, index_of_sentence_2, ...]
        where each index is the index of a sentence where the character is mentioned.
        """

        name_dict = {}

        if not self.name_list:
            self.get_name_list()

        for name in self.name_list:
            name = name[0]
            name_dict[name] = []

            for x in range(len(self.sentences)):
                if name in self.sentences[x]:
                    name_dict[name].append(x)

        self.name_dict = name_dict
        return name_dict

    def get_name_corefs(self):
        """
        This function differs from get_name_corefs in that it is applied to the
        results of the get_mentions_full_charlist.

        It goes through the mention_dictionary and performs coreference resolution
        on each mention. Then it extracts out only those coref clusters with
        the character name as the main attribute of the cluster.

        It returns a coref_dict in the form coref_dict[name] = [cluster1, cluster2, ...]
        """

        if not self.name_dict:
            self.get_mentions_full_charlist()

        name_coref_dict = {}
        for name in self.name_dict.keys():
            name_coref_dict[name] = []
            for mention in self.name_dict[name]:
                mention_string = self.sentences[mention]
                spaced = nlp(mention_string)
                for cluster in spaced._.coref_clusters:
                    cluster_dict = cluster.__dict__
                    other_cluster_dict = {'mentions':[], 'main':""}
                    other_cluster_dict['mentions'] = [mention.text for mention in cluster_dict['mentions']]
                    other_cluster_dict['main'] = cluster.main.text
                    if other_cluster_dict['main'] == name:
                        name_coref_dict[name].append(other_cluster_dict)

        self.name_coref_dict = name_coref_dict
        return name_coref_dict

    def get_aliases(self, get_corefs = False):
        """
        Makes a dictionary of Alias objects for the document, so we know all of the Aliases within the character.

        :param self: The document to get all of the aliases for.
        :param get_corefs: Whether or not we want to get the corefs for each alias. Getting corefs is expensive,
        but we need them to guess genders.
        """

        mention_dict = self.get_mentions_full_charlist()

        if get_corefs:
            if not self.name_coref_dict:
                self.name_coref_dict = self.get_name_corefs()
            for name_and_count in self.name_list:
                name = name_and_count[0]
                count = name_and_count[1]
                alias = Alias.objects.create_alias(name=name, count=count, mentions=mention_dict[name],coref_clusters= self.name_coref_dict[name])
                self.aliases.add(alias)
        else:
            for name_and_count in self.name_list:
                name = name_and_count[0]
                count = name_and_count[1]
                alias = Alias.objects.create_alias(name=name, count=count, mentions=mention_dict[name])
                self.aliases.add(alias)
        self.save()

    def get_disambiguated_characters(self, cutoff_num=20):
        """
        Input: A dictionary of aliases.
        Output: A list of disambiguated Character objects.
        """

        alias_list = list(self.aliases.all())

        for i in range(len(alias_list) - 1):
            new_character = Character.objects.create_character(alias_list[i])
            for j in range(i + 1, len(alias_list)):
                if set(filter_honr(alias_list[i].get_name())).intersection(
                        set(filter_honr(alias_list[j].get_name()))):
                    new_character.add_alias(alias_list[j])

            if sum(alias.count for alias in list(new_character.aliases.all())) > cutoff_num:
                new_character.save()
                self.characters.add(new_character)

        self.save()


    def get_count_of_word(self, word):
        """
        Returns the number of instances of a word in the text.

        Note: This method is not case sensitive

        :param word: word to be counted in text
        :return: Number of occurrences of the word, as an int
        """
        try:
            return self.word_count_counter[word.lower()]
        except KeyError:
            return 0

    def get_count_of_words(self, words):
        """
        A helper method for retrieving the number of occurrences of a given set of words within
        a Document.

        Note: The method is not case sensitive.

        :param words: a list of strings.
        :return: a Counter with each word in words keyed to its number of occurrences.
        """
        return Counter({word: self.get_count_of_word(word) for word in words})

    def find_quoted_text(self):
        """
        Finds all of the quoted statements in the document text.

        :return: List of strings enclosed in double-quotations
        """
        text_list = self.cleaned_text.split()
        quotes = []
        current_quote = []
        quote_in_progress = False
        quote_is_paused = False

        for word in text_list:
            if word[0] == "\"":
                quote_in_progress = True
                quote_is_paused = False
                current_quote.append(word)
            elif quote_in_progress:
                if not quote_is_paused:
                    current_quote.append(word)
                if word[-1] == "\"":
                    if word[-2] != ',':
                        quote_in_progress = False
                        quote_is_paused = False
                        quotes.append(' '.join(current_quote))
                        current_quote = []
                    else:
                        quote_is_paused = True
        return quotes

    def words_associated(self, target_word):
        """
        Returns a Counter of the words found after a given word.

        In the case of double/repeated words, the counter would include the word itself and the next
        new word.

        Note: the method is not case sensitive and words always return lowercase.

        :param target_word: Single word to search for in the document's text
        :return: a Python Counter() object with {associated_word: occurrences}
        """
        target_word = target_word.lower()
        word_count = Counter()
        check = False
        text = self.tokenized_text

        for word in text:
            if check:
                word_count[word] += 1
                check = False
            if word == target_word:
                check = True
        return word_count

    def get_word_windows(self, search_terms, window_size=2):
        """
        Finds all instances of `word` and returns a counter of the words around it.
        window_size is the number of words before and after to return, so the total window is
        2*window_size + 1.

        This is not case sensitive.

        :param search_terms: String or list of strings to search for
        :param window_size: integer representing number of words to search for in either direction
        :return: Python Counter object
        """

        if isinstance(search_terms, str):
            search_terms = [search_terms]

        search_terms = set(i.lower() for i in search_terms)

        counter = Counter()

        for text_window in windowed(self.tokenized_text, 2 * window_size + 1):
            if text_window[window_size] in search_terms:
                for surrounding_word in text_window:
                    if surrounding_word not in search_terms:
                        counter[surrounding_word] += 1

        return counter

    def get_word_freq(self, word):
        """
        Returns the frequency of appearance of a word in the document

        :param word: str to search for in document
        :return: float representing the portion of words in the text that are the parameter word
        """
        word_frequency = self.get_count_of_word(word) / self.word_count
        return word_frequency

    def get_word_freqs(self, words):
        """
        A helper method for retrieving the frequencies of a given set of words within a Document.

        :param words: a list of strings.
        :return: a dictionary of words keyed to float frequencies.
        """
        word_frequencies = {word: self.get_count_of_word(word) / self.word_count for word in words}
        return word_frequencies

    def get_part_of_speech_words(self, words, remove_swords=True):
        """
        A helper method for retrieving the number of occurrences of input words keyed to their
        NLTK tag values (i.e., 'NN' for noun).

        :param words: a list of strings.
        :param remove_swords: optional boolean, remove stop words from return.
        :return: a dictionary keying NLTK tag strings to Counter instances.
        """
        stop_words = set(nltk.corpus.stopwords.words('english'))
        document_pos_tags = self.part_of_speech_tags
        words_set = {word.lower() for word in words}
        output = {}

        for token, tag in document_pos_tags:
            lowered_token = token.lower()
            if remove_swords is True and token in stop_words:
                continue
            if token not in words_set:
                continue
            if tag not in output:
                output[tag] = Counter()
            output[tag][lowered_token] += 1

        return output

    def update_metadata(self, new_metadata):
        """
        Updates the metadata of the document without requiring a complete reloading
        of the text and other properties.

        :param new_metadata: dict of new metadata to apply to the document
        :return: None
        """
        default_fields = [field.name for field in self._meta.get_fields()]
        for key in new_metadata:
            if key not in default_fields:
                self.new_attributes[key] = new_metadata[key]
            else:
                setattr(self, key, new_metadata[key])

        if 'text' in new_metadata:
            self.text = new_metadata['text']
            self.get_tokenized_text_wc_and_pos()
        self.save()


class Corpus(models.Model):
    """
    This model will hold associations to other Documents and their
    metadata (author, title, publication date, etc.)
    """
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500, blank=True)
    documents = models.ManyToManyField(Document)

    class Meta:
        verbose_name_plural = "Corpora"

    def __str__(self):
        """Returns the title of the corpus"""
        return self.title

    def __len__(self):
        """Returns the number of documents associated with this corpus"""
        return len(self.document_set.all())

    def __iter__(self):
        """Yields each document associated with the corpus"""
        for this_document in self.document_set.all():
            yield this_document

    def __eq__(self, other):
        """Returns true if both of the corpora are associated with the same documents"""
        if not isinstance(other, Corpus):
            raise NotImplementedError("Only a Corpus can be compared to another Corpus.")

        if len(self) != len(other):
            return False

        if set(self.document_set.all()) == set(other.document_set.all()):
            return True
        else:
            return False
