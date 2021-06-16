"""
Models for the ***** app.
"""
from django.db import models


class PronounSeries(models.Model):
    """
    A class that allows users to define a custom series of pronouns to be used in
    `gender_analysis` functions
    """

    identifier = models.CharField(max_length=40)

    def __init__(self, identifier, pronouns, subj, obj):
        """
        Creates a new series of pronouns, designated by the given identifier. Pronouns
        are any collection of strings that can be used to identify someone.
        `subj` and `obj` will be considered part of the pronoun series regardless of whether
        they are listed in `pronouns`.
        Note that pronouns are case-insensitive.
        :param identifier: String used to identify what the particular series represents
        :param pronouns: Iterable of Strings that are to be used as pronouns for this group
        :param subj: String used as the "subject" pronoun of the series
        :param obj: String used as the "object" pronoun of the series
        """

        self.identifier = identifier
        self.subj = subj.lower()
        self.obj = obj.lower()

        self.pronouns = {self.subj, self.obj}
        for pronoun in pronouns:
            self.pronouns.add(pronoun.lower())

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

        return pronoun.lower() in self.pronouns

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
        yield from self.pronouns

    def __repr__(self):
        """
        # >>> from gender_analysis import PronounSeries
        >>> PronounSeries('Masc', {'he', 'himself', 'his'}, subj='he', obj='him')
        <Masc: ['he', 'him', 'himself', 'his']>
        :return: A console-friendly representation of the pronoun series
        """

        return f'<{self.identifier}: {sorted(self.pronouns)}>'

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
                and self.pronouns == other.pronouns
                and self.obj == other.obj
                and self.subj == other.subj
        )


class Gender(models.Model):
    """
    This model defines a gender that will be operated on in analysis functions.
    """

    label = models.CharField(max_length=60)

    def __init__(self, label, pronoun_series, names=None):
        """
        Initializes a Gender object that can be used for comparing and contrasting in the
        analysis functions.
        The gender accepts one or more `PronounSeries` that will be used to identify the gender.
        # >>> from gender_analysis import PronounSeries
        # >>> from gender_analysis import Gender
        >>> he_series = PronounSeries('Masc', {'he', 'him', 'his'}, subj='he', obj='him')
        >>> masc_names = ['Andrew', 'Richard', 'Robert']
        >>> male = Gender('Male', he_series, names=masc_names)
        >>> 'Richard' in male.names
        True
        >>> 'robert' in male.names
        False
        >>> 'his' in male.pronouns
        True
        :param label: String name of the gender
        :param pronoun_series: `PronounSeries` or collection of `PronounSeries` that the gender uses
        :param names: A collection of names (as strings) that will be associated with the gender.
            Note that the provided names are case-sensitive.
        """

        self.label = label

        # Allow the user to input a single PronounSeries if only one applies
        if isinstance(pronoun_series, PronounSeries):
            self.pronoun_series = {pronoun_series}
        else:
            self.pronoun_series = set(pronoun_series)

        self.names = set(names) if names is not None else set()

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
                and self.pronoun_series == other.pronoun_series
                and self.names == other.names
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

        pronouns = set()
        for series in self.pronoun_series:
            for pronoun in series:
                pronouns.add(pronoun)

        return pronouns

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

        return self.names | self.pronouns

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
        for series in self.pronoun_series:
            subject_pronouns.add(series.subj)

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

        object_pronouns = set()
        for series in self.pronoun_series:
            object_pronouns.add(series.obj)

        return object_pronouns
