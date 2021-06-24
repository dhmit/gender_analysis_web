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

    # Things to consider:
    # add a default to reflex? i.e. default = object pronoun + 'self'?
    # set blank=True and null=True to PronounSeries? to add for subsequent adding if
    # construction of instances is awkward?
    # Also, how to we run doctests here? Or use pytest? (configs don't recognize django package or relative filepath
    # in import statement)
    identifier = models.CharField(max_length=60)
    subj = LowercaseCharField(max_length=40)
    obj = LowercaseCharField(max_length=40)
    pos_det = LowercaseCharField(max_length=40)
    pos_pro = LowercaseCharField(max_length=40)
    reflex = LowercaseCharField(max_length=40)

    def get_all_pronouns(self):
        """
        :return: The set of all pronoun identifiers.
        """
        all_pronouns = {
            self.subj,
            self.obj,
            self.pos_det,
            self.pos_pro,
            self.reflex,
        }

        return all_pronouns

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

        return pronoun.lower() in self.get_all_pronouns()

    def __iter__(self):
        """
        Allows the user to iterate over all of the pronouns in this group. Pronouns
        are returned in lowercase and order is not guaranteed.
        >>> pronouns = ['she', 'her', 'her', 'hers', 'herself']
        >>> pronoun_group = PronounSeries.objects.create('Fem', *pronouns)
        >>> sorted(pronoun_group)
        ['her', 'hers', 'herself', 'she']
        """

        all_pronouns = self.get_all_pronouns()
        yield from all_pronouns

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
        >>> fem_pronouns = PronounSeries.objects.create('Fem', *['she', 'her', 'her', 'hers', 'herself'])
        >>> Gender('Female', fem_pronouns)
        <Female>
        """

        return f'<{self.label}>'

    def __str__(self):
        """
        :return: A string representation of the gender
        >>> fem_pronouns = PronounSeries.objects.create('Fem', *['she', 'her', 'her', 'hers', 'herself'])
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
        >>> fem_pronouns = PronounSeries.objects.create('Fem', *['she', 'her', 'her', 'hers', 'herself'])
        >>> female = Gender('Female', fem_pronouns)
        >>> another_female = Gender('Female', fem_pronouns)
        >>> female == another_female
        True

        But this one does not:
        >>> they_series = PronounSeries.objects.create('They', *['they', 'them', 'their', 'theirs', 'themselves'])
        >>> xe_series = PronounSeries.objects.create('They', *['Xe', 'Xem', 'Xis', 'Xis', 'Xemself'])
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
        )

    @property
    def pronouns(self):
        """
        :return: A set containing all pronouns that this `Gender` uses
        >>> they_series = PronounSeries.objects.create('They', *['they', 'them', 'their', 'theirs', 'themselves'])
        >>> xe_series = PronounSeries('Xe', *['Xe', 'Xer', 'Xis', 'Xis', 'Xerself'])
        >>> androgynous = Gender.objects.create(label='Androgynous', pronoun_series=[they_series, xe_series])
        >>> androgynous.pronouns == {'they', 'them', 'theirs', 'xe', 'xer', 'xis'}
        True
        """

        all_pronouns = set()
        for series in list(self.pronoun_series.all()):
            for series_pronouns in series.get_all_pronouns():
                all_pronouns |= series_pronouns

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
