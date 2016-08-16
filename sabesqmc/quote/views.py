from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

# Create your views here.
from .models import Quote
from .forms import QuoteForm

def random(request):
    """
    Shows a random message
    """
    quote = Quote()
    random_quote = quote.get_random_msg()
    redirect('message', args=[random_quote.id])

class MessageView(DetailView):
    context_object_name = 'quote'
    queryset = Quote.objects.all()


class MostVotedView(ListView):
    queryset = Quote.objects.approved().order_by('-votes')
    context_object_name = 'quote_list'
    paginate_by = 10


class RecentView(ListView):
    queryset = Quote.objects.approved().order_by('-date_created')
    context_object_name = 'quote_list'
    paginate_by = 10
