# coding: utf-8

from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse

from ..models import Quote

from ..views import (
    RandomQuoteView,
    QuoteDetailView,
    MostVotedView,
    RecentView,
)

class TestQuoteDetailView(TestCase):

    def setUp(self):
        Quote.objects.get_or_create(message="Me caga probar esto", votes=3)
        Quote.objects.get_or_create(message="Me caga probar esto una vez", votes=2)
        Quote.objects.get_or_create(message="Me caga probar esto mas veces", votes=-4)
        Quote.objects.get_or_create(message="Me caga probar esto muchas veces", votes=5)
        self.client = Client()

    def test_get_random_quote(self):
        response = self.client.get('/')
        self.assertEqual(302, response.status_code)

    def test_get_quote(self):
        """
        Test the list view
        """
        quote = Quote.objects.latest('id')
        response = self.client.get(reverse('quote', args=[quote.pk]))
        self.assertEqual(200, response.status_code)


class TestMostVotedView(TestCase):

    def setUp(self):
        Quote.objects.get_or_create(message="Me caga probar esto", votes=3)
        Quote.objects.get_or_create(message="Me caga probar esto una vez", votes=2)
        Quote.objects.get_or_create(message="Me caga probar esto mas veces", votes=-4)
        Quote.objects.get_or_create(message="Me caga probar esto muchas veces", votes=5)
        self.client = Client()
        self.factory = RequestFactory()
        self.view = MostVotedView

    def test_get_list(self):
        """
        Test the list of most voted
        """
        response = self.client.get(reverse('top'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.context[-1]['quote_list']))
        top = response.context[-1]['quote_list'][0].message
        second = response.context[-1]['quote_list'][1].message
        self.assertEqual(top, "Me caga probar esto muchas veces")
        self.assertEqual(second, "Me caga probar esto")

    def test_no_unapproved(self):
        """
        Tests that unapproved quotes are not shown in listings
        """
        request = self.factory.get(reverse('top'))
        response = self.view.as_view()(request)
        bad_quote = Quote.objects.get(votes=-4)
        self.assertNotIn(bad_quote, response.context_data['quote_list'])

class TestRecentView(TestCase):

    def setUp(self):
        Quote.objects.get_or_create(message="Me caga probar esto", votes=3)
        Quote.objects.get_or_create(message="Me caga probar esto una vez", votes=2)
        Quote.objects.get_or_create(message="Me caga probar esto mas veces", votes=-4)
        Quote.objects.get_or_create(message="Me caga probar esto muchas veces", votes=5)
        self.client = Client()

    def test_get_list(self):
        """
        Test the list of recent quotes
        """
        response = self.client.get(reverse('latest'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.context[-1]['quote_list']))
        first = response.context[-1]['quote_list'][0]
        second = response.context[-1]['quote_list'][1]
        self.assertTrue(second.date_created < first.date_created)

    def test_no_unapproved(self):
        """
        Tests that unapproved quotes are not shown in listings
        """
        response = self.client.get(reverse('latest'))
        bad_quote = Quote.objects.get(votes=-4)
        self.assertNotIn(bad_quote, response.context[-1]['quote_list'])
