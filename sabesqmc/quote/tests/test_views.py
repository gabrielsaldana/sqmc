from django.test import RequestFactory
from django.test import TestCase

from ..views import (
    random,
    MessageView,
    MostVotedView,
    RecentView,
)

class TestQuotesView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_random(self):
        request = self.factory.get('/')


class TestMessageView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = MessageView()

    def test_get_list(self):
        """
        Test the list view
        """
        pass


class TestMostVotedView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = MostVotedView()

    def test_get_list(self):
        """
        Test the list of most voted
        """
        pass


class TestRecentView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = RecentView()

    def test_get_list(self):
        """
        Test the list of recent quotes
        """
        pass
