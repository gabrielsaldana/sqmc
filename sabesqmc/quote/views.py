from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView


# Create your views here.
from .models import Quote
from .forms import QuoteForm


class RandomQuoteView(RedirectView):
    """
    Shows a random message
    """
    pattern_name = 'quote'

    def get_redirect_url(self, *args, **kwargs):
        quote = Quote.objects.get_random()
        return super(RandomQuoteView, self).get_redirect_url(quote.pk, **kwargs)


class QuoteCreateView(CreateView):
    """
    Create a new message
    """
    model = Quote
    form_class = QuoteForm
    template_name = 'new.html'

    def get_success_url(self):
        return reverse('quote', args=(self.object.id,))


class QuoteDetailView(DetailView):
    """
    Show a specific message
    """
    context_object_name = 'quote'
    template_name = 'detail.html'
    model = Quote

    def get_context_data(self, **kwargs):
        context = super(QuoteDetailView, self).get_context_data(**kwargs)
        context['form'] = QuoteForm()
        return context


class MostVotedView(ListView):
    """
    List the most voted messages
    """
    model = Quote
    queryset = Quote.objects.approved().order_by('-votes')
    context_object_name = 'quote_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MostVotedView, self).get_context_data(**kwargs)
        context['list_type'] = 'votadas'
        return context


class RecentView(ListView):
    """
    List the recently added messages
    """
    model = Quote
    queryset = Quote.objects.approved().order_by('-date_created')
    context_object_name = 'quote_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(RecentView, self).get_context_data(**kwargs)
        context['list_type'] = 'recientes'
        return context
