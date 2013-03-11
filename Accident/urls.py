__author__ = 'Behnam Hatami'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^home$', 'Accident.views.home', name="home"),
                       url(r'^create_accident$', 'Accident.views.create_accident', name='create_accident'),
                       url(r'^(?P<aid>\d+)/finalize$', 'Accident.views.finalize_accident', name='finalize_accident'),
                       url(r'^(?P<aid>\d+)/$', 'Accident.views.view_accident', name='view_accident'),
                       url(r'^$', 'Accident.views.accident', name='accident'),
)
