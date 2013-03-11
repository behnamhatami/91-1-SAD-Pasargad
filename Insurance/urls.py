__author__ = 'Behnam Hatami'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^home$', 'Insurance.views.home', name='home'),
                       url(r'^contract/(?P<cid>\d+)/vehicle/(?P<vid>\d+)/history$', 'Insurance.views.history_vehicle',
                           name='history_vehicle'),
                       url(r'^contract/(?P<cid>\d+)/vehicle/(?P<vid>\d+)/edit$', 'Insurance.views.edit_vehicle',
                           name='edit_vehicle'),
                       url(r'^contract/(?P<cid>\d+)/vehicle/(?P<vid>\d+)$', 'Insurance.views.view_vehicle',
                           name='view_vehicle'),

                       url(r'^contract/(?P<cid>\d+)/person/(?P<pid>\d+)/history$', 'Insurance.views.history_person',
                           name='history_person'),
                       url(r'^contract/(?P<cid>\d+)/person/(?P<pid>\d+)/edit$', 'Insurance.views.edit_person',
                           name='edit_person'),
                       url(r'^contract/(?P<cid>\d+)/person/(?P<pid>\d+)$', 'Insurance.views.view_person',
                           name='view_person'),

                       url(r'^contract/(?P<cid>\d+)/company/(?P<mid>\d+)/history$', 'Insurance.views.history_company',
                           name='history_company'),
                       url(r'^contract/(?P<cid>\d+)/company/(?P<mid>\d+)/edit$', 'Insurance.views.edit_company',
                           name='edit_company'),
                       url(r'^contract/(?P<cid>\d+)/company/(?P<mid>\d+)$', 'Insurance.views.view_company',
                           name='view_company'),

                       url(r'^contract/(?P<cid>\d+)/history$', 'Insurance.views.history_contract',
                           name='history_contract'),
                       url(r'^contract/(?P<cid>\d+)/edit$', 'Insurance.views.edit_contract', name='edit_contract'),
                       url(r'^contact/(?P<cid>\d+)/accidents$', 'Insurance.views.list_accident', name='list_accident'),
                       url(r'^contract/(?P<cid>\d+)/print$', 'Insurance.views.print_contract', name='print_contract'),
                       url(r'^contract/(?P<cid>\d+)$', 'Insurance.views.view_contract', name='view_contract'),
                       url(r'^contract/create$', 'Insurance.views.create_contract', name='create_contract'),
                       url(r'^contract/search_contract$', 'Insurance.views.search_contract', name='search_contract'),
                       url(r'^contract$', 'Insurance.views.contract', name='contract'),
)
