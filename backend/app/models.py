"""
Models for the gender analysis web app.
"""
from django.db import models
from .fields import LowercaseCharField


class Pronoun(models.Model):
    """
    A model that allows users to define an individual pronoun and its type
    (e.g. subject, object, reflexive, etc). Pronouns are case-insensitive and will be
    converted to lowercase.
    """
    PRONOUN_TYPES = [
        ('subj', 'Subject'),
        ('obj', 'Object'),
        ('pos_det', 'Possessive determiner'),
        ('pos_pro', 'Possessive pronoun'),
        ('reflex', 'Reflexive'),
    ]

    identifier = LowercaseCharField(max_length=40)
    type = models.CharField(max_length=7, choices=PRONOUN_TYPES)

    def __repr__(self):
        return f'Pronoun({self.identifier, self.type})'

    def __str__(self):
        pronoun_type_str = ''

        for PRONOUN_TYPE in Pronoun.PRONOUN_TYPES:
            if PRONOUN_TYPE[0] == self.type:
                pronoun_type_str = PRONOUN_TYPE[1]
                break

        return (
            f'Pronoun: {self.identifier}\nType: {pronoun_type_str}'
        )

    def __hash__(self):
        """
        Makes the `Pronoun` model hashable
        """
        return self.identifier.__hash__()

    # Ideally, __eq__ should only be called after a Model instance is saved to the database;
    # how do we ensure this?
    def __eq__(self, other):
        return self.identifier == other.identifier and self.type == other.type

class PronounSeries(models.Model):
    """
    A class that allows users to define a custom series of pronouns to be used in
    `gender_analysis` functions
    """


    identifier = models.CharField(max_length=60)
    pronouns = models.ManyToManyField(Pronoun)
    # subj = LowercaseCharField(max_length=40)
    # obj = LowercaseCharField(max_length=40)

    def __contains__(self, pronoun):
        """
        Checks to see if the given pronoun exists in this group. This check is case-insensitive
        # >>> from gender_analysis import PronounSeries
        >>> pronouns = {'They', 'Them', 'Theirs', 'Themself'}
        >>> pronoun_group = PronounSeries('Andy', pronouns, 'they', 'them')
        >>> 'they' in pronoun_group
        True
        >>> 'hers' in pronoun_group
        False
        :param pronoun: The pronoun to check for in this group
        :return: true if the pronoun is in the group, false otherwise
        """

        for each_pronoun in list(self.pronouns.all()):
            if pronoun.lower() == each_pronoun.identifier:
                return True
        return False

    def __iter__(self):
        """
        Allows the user to iterate over all of the pronouns in this group. Pronouns
        are returned in lowercase and order is not guaranteed.
        # >>> from gender_analysis import PronounSeries
        >>> pronouns = {'She', 'Her', 'hers', 'herself'}
        >>> pronoun_group = PronounSeries('Fem', pronouns, subj='she', obj='her')
        >>> sorted(pronoun_group)
        ['her', 'hers', 'herself', 'she']
        """

        all_pronouns = []
        for each_pronoun in list(self.pronouns.all()):
            all_pronouns.append(each_pronoun.identifier)
        yield from all_pronouns

    def __repr__(self):
        """
        # >>> from gender_analysis import PronounSeries
        >>> PronounSeries('Masc', {'he', 'himself', 'his'}, subj='he', obj='him')
        <Masc: ['he', 'him', 'himself', 'his']>
        :return: A console-friendly representation of the pronoun series
        """

        return f'{self.identifier}: {list(self.pronouns.all())}'

    def __str__(self):
        """
        # >>> from gender_analysis import PronounSeries
        >>> str(PronounSeries('Andy', {'Xe', 'Xis', 'Xem'}, subj='xe', obj='xem'))
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
        # >>> from gender_analysis import PronounSeries
        >>> fem_series = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> second_fem_series = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> fem_series == second_fem_series
        True
        >>> masc_series = PronounSeries('Masc', {'he', 'him', 'his'}, subj='he', obj='him')
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
    This model defines a gender that will be operated on in analysis functions.
    """

    label = models.CharField(max_length=60)

    #Many to many relationship with Pronoun Series model, but there will be only one pronoun series. This can potentially allow us to integrate multiple pronouns from the pronoun series model.
    pronoun_series = models.ManyToManyField(PronounSeries)

    def __repr__(self):
        """
        :return: A console-friendly representation of the gender
        # >>> from gender_analysis import PronounSeries
        # >>> from gender_analysis import Gender
        >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> Gender('Female', fem_pronouns)
        <Female>
        """

        return f'<{self.label}>'

    def __str__(self):
        """
        :return: A string representation of the gender
        # >>> from gender_analysis import PronounSeries
        # >>> from gender_analysis import Gender
        >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> str(Gender('Female', fem_pronouns))
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
        # >>> from gender_analysis import PronounSeries
        # >>> from gender_analysis import Gender
        >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> female = Gender('Female', fem_pronouns)
        >>> another_female = Gender('Female', fem_pronouns)
        >>> female == another_female
        True
        But this one does not:
        # >>> from gender_analysis import PronounSeries
        # >>> from gender_analysis import Gender
        >>> they_series = PronounSeries('They', {'they', 'them', 'theirs'}, subj='they', obj='them')
        >>> xe_series = PronounSeries('Xe', {'xe', 'xer', 'xem'}, subj='xe', obj='xem')
        >>> androgynous_1 = Gender('NB', they_series)
        >>> androgynous_2 = Gender('NB', xe_series)
        >>> androgynous_1 == androgynous_2
        False
        :param other: The other `Gender` object to compare
        :return: `True` if the `Gender`s are the same, `False` otherwise
        """

        return (
                self.label == other.label
                and list(self.pronoun_series.all())[0] == other.pronoun_series.all()
        )

    @property
    def pronouns(self):
        """
        :return: A set containing all pronouns that this `Gender` uses
        # >>> from gender_analysis import PronounSeries
        # >>> from gender_analysis import Gender
        >>> they_series = PronounSeries('They', {'they', 'them', 'theirs'}, subj='they', obj='them')
        >>> xe_series = PronounSeries('Xe', {'Xe', 'Xer', 'Xis'}, subj='xe', obj='xer')
        >>> androgynous = Gender('Androgynous', [they_series, xe_series])
        >>> androgynous.pronouns == {'they', 'them', 'theirs', 'xe', 'xer', 'xis'}
        True
        """

        all_pronouns = set()
        for series in list(self.pronoun_series.all()):
            for pronoun in list(series.pronouns.all()):
                all_pronouns.add(pronoun)
        return all_pronouns

    @property
    def identifiers(self):
        """
        :return: Set of all words (i.e. pronouns and names) that are used to identify the gender
        # >>> from gender_analysis import PronounSeries
        # >>> from gender_analysis import Gender
        >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> fem_names = {'Sarah', 'Marigold', 'Annabeth'}
        >>> female = Gender('Female', fem_pronouns, fem_names)
        >>> female.identifiers == {'she', 'her', 'hers', 'Sarah', 'Marigold', 'Annabeth'}
        True
        """
        # names need to be taken care of
        return self.pronouns

    @property
    def subj(self):
        """
        :return: set of all subject pronouns used to describe the gender
        # >>> from gender_analysis import PronounSeries
        # >>> from gender_analysis import Gender
        >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> masc_pronouns = PronounSeries('Masc', {'he', 'him', 'his'}, subj='he', obj='him')
        >>> bigender = Gender('Bigender', [fem_pronouns, masc_pronouns])
        >>> bigender.subj == {'he', 'she'}
        True
        """

        subject_pronouns = set()
        for series in list(self.pronoun_series.all()):
            for each_pronoun in list(series.pronouns.all()):
                if each_pronoun.type == 'subj':
                    subject_pronouns.add(each_pronoun)
        return subject_pronouns

    @property
    def obj(self):
        """
        :return: set of all object pronouns used to describe the gender
        # >>> from gender_analysis import PronounSeries
        # >>> from gender_analysis import Gender
        >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
        >>> masc_pronouns = PronounSeries('Masc', {'he', 'him', 'his'}, subj='he', obj='him')
        >>> bigender = Gender('Bigender', [fem_pronouns, masc_pronouns])
        >>> bigender.obj == {'him', 'her'}
        True
        """

        subject_pronouns = set()
        for series in list(self.pronoun_series.all()):
            for each_pronoun in list(series.pronouns.all()):
                if each_pronoun.type == 'obj':
                    subject_pronouns.add(each_pronoun)
        return subject_pronouns
