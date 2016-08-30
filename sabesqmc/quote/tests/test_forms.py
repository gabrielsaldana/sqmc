# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.test import TestCase

from ..forms import QuoteForm

class TestQuoteForm(TestCase):

    def setUp(self):
        pass

    def test_validate_emtpy_quote(self):
        form = QuoteForm({'message': ''})
        self.assertFalse(form.is_valid())
        form = QuoteForm({'message': '  '})
        self.assertFalse(form.is_valid())

    def test_validate_invalid_quote(self):
        form = QuoteForm({'message': 'Mensaje invalido'})
        self.assertFalse(form.is_valid())
        form = QuoteForm({'message': 'mensaje invalido'})
        self.assertFalse(form.is_valid())
        form = QuoteForm({'message': 'me nsaje invalido'})
        self.assertFalse(form.is_valid())

    def test_urls_in_quote(self):
        form = QuoteForm({'message': 'http://122.33.43.322'})
        self.assertFalse(form.is_valid())
        form = QuoteForm({'message': 'Me caga http://sabesquemecaga.com'})
        self.assertFalse(form.is_valid())
        form = QuoteForm({'message': 'http://sabesquemecaga.com'})
        self.assertFalse(form.is_valid())
        form = QuoteForm({'message': 'http://sabesquemecaga.com/asdfads/'})
        self.assertFalse(form.is_valid())
        form = QuoteForm({'message': 'Me caga http://www.sabesquemecaga.com'})
        self.assertFalse(form.is_valid())
        form = QuoteForm({'message': 'Me caga http://www.sabesquemecaga.com/test/12'})
        self.assertFalse(form.is_valid())

    def test_emails_in_quote(self):
        form = QuoteForm({'message': 'Me caga test@test.com'})
        self.assertFalse(form.is_valid())
        form = QuoteForm({'message': 'Me caga test.this@test.asdfas.com'})
        self.assertFalse(form.is_valid())

    def test_validate_short_quote(self):
        form = QuoteForm({'message': 'Me caga '})
        self.assertFalse(form.is_valid())

    def test_validate_long_quote(self):
        form = QuoteForm({'message': 'Me caga que sea que Este mensaje es demasiado largo y no pase las pruebas de lo que tenemos que probar asdfadfa adsfasdfa. Me caga que sea que Este mensaje es demasiado largo y no pase las pruebas de lo que tenemos que probar.'})
        self.assertFalse(form.is_valid())

    def test_valid_message(self):
        form = QuoteForm({'message': 'Me caga probar esto'})
        self.assertTrue(form.is_valid())
