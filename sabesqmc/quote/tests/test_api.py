# coding: utf-8
import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from ..models import Quote

class VotesTests(APITestCase):

    def setUp(self):
        """
        Set up user for authenticated tests
        """
        test_user = get_user_model().objects.create_user(
            'testuser',
            'test@test.com',
            'testingpass')
        self.client.login(username='testuser', password='testingpass')

    def test_vote(self):
        """
        Ensure we can vote up or down a quote
        """
        test_quote = Quote(message="Me caga probar esto")
        test_quote.save()

        url = reverse('quotes:votes', kwargs={'pk': 1})
        data = {'direction': 'up'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'votes': 1})
        data = {'direction': 'down'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'votes': 0})
