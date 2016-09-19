# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import re

from django import forms
from django.core import validators
from django.db import IntegrityError
from django.forms import ModelForm

from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

from .models import Quote

class QuoteForm(ModelForm):
    """
    Form for sending a new message
    """
    message = forms.CharField(label='Desahógate aquí',
                              max_length=140,
                              initial='Me caga ')

    class Meta:
        model = Quote
        fields = ['message',]

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Field('message', style="width: 680px;"),
            StrictButton('Enviar', type="submit", name="submit-btn", css_class="btn-primary")
        )

    def clean_message(self):
        """
        Checks for a valid message
        """
        quote = self.cleaned_data['message']
        if not quote:
            raise forms.ValidationError("Me caga que intentes enviar un mensaje vacío.")
        # check for quotes without the primary words
        phrase = re.compile(r'me\s+caga', re.I)
        if not phrase.match(quote):
            raise forms.ValidationError("Mensaje inválido. Sólo dinos qué te caga.")
        # check for short or empty quote
        if quote.lower() == 'me caga' or len(quote) <= 7:
            raise forms.ValidationError("Tu mensaje es demasiado corto.")
        # check for long quotes
        if len(quote) > 140:
            raise forms.ValidationError("Tu mensaje esta demasiado largo. Dinos qué te caga en 140 caracteres.")
        # check for urls
        if re.search(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?', quote):
            raise forms.ValidationError("A mi me caga que pongas URLs en tu mensaje.")
        # check for emails
        if re.search(r'([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})', quote):
            raise forms.ValidationError('Me caga que pongas emails en tu mensaje.')
        return self.cleaned_data['message']
