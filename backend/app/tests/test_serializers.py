"""
Tests for the serializers of the gender analysis web app.
"""
from django.test import TestCase

from ..models import (
    PronounSeries,
    Gender,
)
from ..serializers import (
    PronounSeriesSerializer,
    GenderSerializer,
)


class PronounSeriesSerializerTestCase(TestCase):
    """
    TestCase for the PronounSeries serializer.
    """

    def setUp(self):
        PronounSeries.objects.create(
            identifier='Male',
            subj='he',
            obj='him',
            pos_det='his',
            pos_pro='his',
            reflex='himself'
        )

        PronounSeries.objects.create(
            identifier='Female',
            subj='she',
            obj='her',
            pos_det='her',
            pos_pro='hers',
            reflex='herself'
        )

    def test_serialization(self):
        pass


class GenderSerializerTestCase(TestCase):
    """
    TestCase for the Gender serializer.
    """

    def setUp(self):
        PronounSeries.objects.create(
            identifier='Male',
            subj='he',
            obj='him',
            pos_det='his',
            pos_pro='his',
            reflex='himself'
        )

        PronounSeries.objects.create(
            identifier='Female',
            subj='she',
            obj='her',
            pos_det='her',
            pos_pro='hers',
            reflex='herself'
        )

        Gender.objects.create(label='Man 1')
        Gender.objects.create(label='Woman 1')
        Gender.objects.create(label='Male/Female')

    def test_serialization(self):
        pass
