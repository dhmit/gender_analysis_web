"""
Models for the gender analysis web app.
"""
from django.db import models
from .fields import LowercaseCharField


class PronounSeries(models.Model):
    """
    A class that allows users to define a custom series of pronouns to be used in
    analysis functions
    """

    identifier = models.CharField(max_length=60)
    subj = LowercaseCharField(max_length=40, blank=True)
    obj = LowercaseCharField(max_length=40, blank=True)
    pos_det = LowercaseCharField(max_length=40, blank=True)
    pos_pro = LowercaseCharField(max_length=40, blank=True)
    reflex = LowercaseCharField(max_length=40, blank=True)

    # def get_all_pronouns(self):
    #     """
    #     :return: The set of all pronoun identifiers.
    #     """
    #     all_pronouns = {
    #         self.subj.identifier,
    #         self.obj.identifier,
    #         self.pos_det.identifier,
    #         self.pos_pro.identifier,
    #         self.reflex.identifier,
    #     }
    #
    #     return all_pronouns

    # def __contains__(self, pronoun):
    #     """
    #     Checks to see if the given pronoun exists in this group. This check is case-insensitive
    #     # >>> from gender_analysis import PronounSeries
    #     >>> pronouns = {'They', 'Them', 'Theirs', 'Themself'}
    #     >>> pronoun_group = PronounSeries('Andy', pronouns, 'they', 'them')
    #     >>> 'they' in pronoun_group
    #     True
    #     >>> 'hers' in pronoun_group
    #     False
    #     :param pronoun: The pronoun to check for in this group
    #     :return: True if the pronoun is in the group, False otherwise
    #     """
    #
    #     return pronoun.lower() in self.get_all_pronouns()

    # def __iter__(self):
    #     """
    #     Allows the user to iterate over all of the pronouns in this group. Pronouns
    #     are returned in lowercase and order is not guaranteed.
    #     # >>> from gender_analysis import PronounSeries
    #     >>> pronouns = {'She', 'Her', 'hers', 'herself'}
    #     >>> pronoun_group = PronounSeries('Fem', pronouns, subj='she', obj='her')
    #     >>> sorted(pronoun_group)
    #     ['her', 'hers', 'herself', 'she']
    #     """
    #
    #     all_pronouns = self.get_all_pronouns()
    #     yield from all_pronouns

    def __repr__(self):
        """
        >>> PronounSeries.create(
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

        >>> fem_series = PronounSeries.create(
        ...     identifier='Fem',
        ...     subj='she',
        ...     obj='her',
        ...     pos_det='her',
        ...     pos_pro='hers',
        ...     reflex='herself'
        ... )
        >>> second_fem_series = PronounSeries.create(
        ...     identifier='Fem',
        ...     subj='she',
        ...     obj='her',
        ...     pos_pro='hers',
        ...     reflex='herself'
        ...     pos_det='HER',
        ... )
        >>> fem_series == second_fem_series
        True
        >>> masc_series = PronounSeries.create(
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
                and list(self.pronoun_series.all()) == list(other.pronoun_series.all())
                and list(self.names_series.all()) == list(other.names_series.all())
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

    # These may be better off in the PronounSeries model, if they exist at all

    # @property
    # def subj(self):
    #     """
    #     :return: set of all subject pronouns used to describe the gender
    #     # >>> from gender_analysis import PronounSeries
    #     # >>> from gender_analysis import Gender
    #     >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
    #     >>> masc_pronouns = PronounSeries('Masc', {'he', 'him', 'his'}, subj='he', obj='him')
    #     >>> bigender = Gender('Bigender', [fem_pronouns, masc_pronouns])
    #     >>> bigender.subj == {'he', 'she'}
    #     True
    #     """
    #
    #     subject_pronouns = set()
    #     for series in list(self.pronoun_series.all()):
    #         for each_pronoun in list(series.pronouns.all()):
    #             if each_pronoun.type == 'subj':
    #                 subject_pronouns.add(each_pronoun)
    #     return subject_pronouns
    #
    # @property
    # def obj(self):
    #     """
    #     :return: set of all object pronouns used to describe the gender
    #     # >>> from gender_analysis import PronounSeries
    #     # >>> from gender_analysis import Gender
    #     >>> fem_pronouns = PronounSeries('Fem', {'she', 'her', 'hers'}, subj='she', obj='her')
    #     >>> masc_pronouns = PronounSeries('Masc', {'he', 'him', 'his'}, subj='he', obj='him')
    #     >>> bigender = Gender('Bigender', [fem_pronouns, masc_pronouns])
    #     >>> bigender.obj == {'him', 'her'}
    #     True
    #     """
    #
    #     subject_pronouns = set()
    #     for series in list(self.pronoun_series.all()):
    #         for each_pronoun in list(series.pronouns.all()):
    #             if each_pronoun.type == 'obj':
    #                 subject_pronouns.add(each_pronoun)
    #     return subject_pronouns


class Document(models.Model):
    """
    This model will hold the full text and
    metadata (author, title, publication date, etc.) of a document
    """
    author = models.CharField(max_length=255, blank=True)
    date = models.IntegerField(null=True, blank=True)
    new_attributes = models.JSONField(null=True, blank=True, default=dict)
    text = models.TextField(blank=True)
    title = models.CharField(max_length=255, blank=True)
    word_count = models.PositiveIntegerField(blank=True, null=True, default=None)
    tokenized_text = models.JSONField(null=True, blank=True, default=None)
    word_counts_counter = models.JSONField(null=True, blank=True, default=dict)
    part_of_speech_tags = models.JSONField(null=True, blank=True, default=list)
