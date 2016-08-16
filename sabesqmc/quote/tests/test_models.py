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
        self.assertEqual(quote.get_absolute_url(), '/1/')

    def test_get_random(self):
        random = Quote.objects.get_random()
        self.assertTrue(random)

    def test_approved(self):
        #generate two quotes, one with more than 3 down votes
        quote1 = Quote(message="Me caga probar esto")
        quote1.save()
        quote2 = Quote(message="Me caga probar esto otra vez", votes=-4)
        quote2.save()
        # check all got saved
        self.assertEqual(3, Quote.objects.all().count())
        # check approved filtering
        self.assertEqual(2, Quote.objects.approved().count())
