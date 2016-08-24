# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from random import randrange

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
class QuoteManager(models.Manager):

    use_for_related_fields = True

    def get_random(self):
        """
        Gets a random message from database
        """
        size = int(self.latest('id').id)
        quote = None
        while not quote:
            rand_id = randrange(1,size)
            try:
                quote = self.approved().get(pk=rand_id)
                if quote:
                    break
            except Quote.DoesNotExist:
                continue
        return quote

    def approved(self):
        return self.exclude(votes__lt=-3)

@python_2_unicode_compatible
class Quote(models.Model):
    message = models.CharField(max_length=140, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    is_annonymous = models.BooleanField(default=1, blank=True)
    votes = models.IntegerField(default=0, null=True, blank=True)

    objects = QuoteManager()

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return "%s" % self.message

    def get_absolute_url(self):
        return reverse('quote', args=[self.id])

    def vote(self, how):
        if how == "up":
            self.votes += 1
        elif how == "down":
            self.votes -= 1
        self.save()
        return self.votes
