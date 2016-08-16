from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.random, name='homepage'),
    url(r'^(?P<msg_id>\d+)/$', views.MessageView.as_view(), name='message')
    url(r'^ultimas/$', views.RecentView.as_view(), name='latest')
    url(r'^top/$', views.MostVotedView.as_view(), name='top')
]
