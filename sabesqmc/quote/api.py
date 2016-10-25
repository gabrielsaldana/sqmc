# coding: utf-8
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import User

from .models import Quote


class Votes(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Returns the votes on a given quote id
        """
        quote_id = int(request.GET.get('quote'))
        quote = get_object_or_404(Quote, pk=quote_id)
        return Response(quote.votes)

    def put(self, request, pk, format=None):
        """
        Sends a vote to a given quote
        """
        quote_id = pk
        direction = request.POST.get('direction')
        quote = get_object_or_404(Quote, pk=quote_id)
        votes = quote.vote(direction)
        quote.save()
        return Response({'votes': quote.votes})
