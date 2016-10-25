# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.test import TestCase

from ..models import Quote

# Create your tests here.
class TestQuote(TestCase):

    def setUp(self):
        pass

    def test__str__(self):
        quote = Quote()
        quote.message = 'Me cagan las pruebas'
        quote.save()
        self.assertEqual(quote.__str__(), 'Me cagan las pruebas')

    def test_get_absolute_url(self):
        quote = Quote()
        quote.message = 'Me cagan las pruebas'
        quote.save()
        self.assertEqual(quote.get_absolute_url(), '/%s/' % quote.pk)

    def test_get_random(self):
        quote1 = Quote(message="Me caga probar esto")
        quote1.save()
        quote2 = Quote(message="Me caga probar esto otra vez")
        quote2.save()
        quote3 = Quote(message="Me caga probar esto dos veces")
        quote3.save()
        quote4 = Quote(message="Me caga probar esto tres veces")
        quote4.save()
        random = Quote.objects.get_random()
        self.assertTrue(random)

    def test_approved(self):
        #generate two quotes, one with more than 3 down votes
        quote1 = Quote(message="Me caga probar esto")
        quote1.save()
        quote2 = Quote(message="Me caga probar esto otra vez", votes=-4)
        quote2.save()
        # check all got saved
        self.assertEqual(2, Quote.objects.all().count())
        # check approved filtering
        self.assertEqual(1, Quote.objects.approved().count())

    def test_vote(self):
        quote1 = Quote(message="Me caga probar esto")
        quote1.save()
        self.assertEqual(0, quote1.votes)
        quote1.vote('up')
        self.assertEqual(1, quote1.votes)
        quote1.vote('down')
        self.assertEqual(0, quote1.votes)
