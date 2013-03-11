__author__ = 'Behnam Hatami'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^home$', 'Statistic.views.home', name='home'),
                       url(r'^general$', 'Statistic.views.general_payments', name='general'),
                       url(r'^user$', 'Statistic.views.user_payments', name='user'),
                       url(r'owner$', 'Statistic.views.owner_payments', name='owner'),
                       url(r'accidents', 'Statistic.views.accidents', name='accident'),
)



