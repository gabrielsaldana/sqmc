# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import re

from django import forms
from django.core import validators
from django.db import IntegrityError

from .models import Quote

class QuoteForm(forms.Form):
    """
    Form for sending a new message
    """
    quote = forms.CharField(max_length=140, initial='Me caga ')
    is_annonymous = forms.BooleanField(required=False,
                                       widget=forms.CheckboxInput())

    def clean(self):
        """
        Checks for a valid message
        """
        quote = self.cleaned_data['quote']
        if not quote:
            raise forms.ValidationError("No puedes enviar un mensaje vacío.")
        # check for quotes without the primary words
        phrase = re.compile(r'me\s+caga', re.I)
        if not phrase.match(quote):
            raise forms.ValidationError("Mensaje inválido. Sólo dinos qué te caga")
        # check for short or empty quote
        if quote.lower() == 'me caga' or len(quote) <= 7:
            raise forms.ValidationError("Tu mensaje es demasiado corto.")
        # check for long quotes
        if len(quote) > 140:
            raise forms.ValidationError("Tu mensaje esta demasiado largo. Dinos qué te caga en 140 caracteres.")
        return self.cleaned_data
