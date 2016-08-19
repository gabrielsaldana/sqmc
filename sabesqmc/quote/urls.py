from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RandomQuoteView.as_view(), name='homepage'),
    url(r'^(?P<pk>\d+)/$', views.QuoteDetailView.as_view(), name='quote'),
    url(r'^ultimas/$', views.RecentView.as_view(), name='latest'),
    url(r'^top/$', views.MostVotedView.as_view(), name='top'),
]
