__author__ = 'Behnam Hatami'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^home$', 'Home.views.home', name="home"),
                       )