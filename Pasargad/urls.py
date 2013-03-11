from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Pasargad.views.home', name='home'),
    # url(r'^Pasargad/', include('Pasargad.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('Account.urls', namespace='Account')),
    url(r'^insurance/', include('Insurance.urls', namespace='Insurance')),
    url(r'^management/', include('Management.urls', namespace='Management')),
    url(r'^Accident/', include('Accident.urls', namespace='Accident')),
    url(r'^Statistic/', include('Statistic.urls', namespace='Statistic')),
    url(r'^', include('Home.urls', namespace='Home')),
)
