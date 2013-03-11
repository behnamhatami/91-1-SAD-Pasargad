__author__ = 'Behnam Hatami'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^home$', 'Management.views.home', name='home'),
                       url(r'^strategy/create$', 'Management.views.create_strategy', name='create_strategy'),
                       url(r'^strategy/(?P<stid>\d+)/edit$', 'Management.views.edit_strategy', name='edit_strategy'),
                       url(r'^strategy/(?P<stid>\d+)/delete$', 'Management.views.delete_strategy',
                           name='delete_strategy'),
                       url(r'^strategy/(?P<stid>\d+)$', 'Management.views.view_strategy', name='view_strategy'),
                       url(r'^strategy$', 'Management.views.strategy', name='strategy'),
                       url(r'^plan/create$', 'Management.views.create_plan', name='create_plan'),
                       url(r'^plan/(?P<pid>\d+)/edit$', 'Management.views.edit_plan', name='edit_plan'),
                       url(r'^plan/(?P<pid>\d+)/delete$', 'Management.views.delete_plan', name='delete_plan'),
                       url(r'^plan/(?P<pid>\d+)$', 'Management.views.view_plan', name='view_plan'),
                       url(r'^plan$', 'Management.views.plan', name='plan'),
)



