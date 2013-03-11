__author__ = 'Behnam Hatami'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^home$', 'Account.views.home', name="home"),
                       url(r'^logout$', 'Account.views.my_logout', name="logout"),
                       url(r'^view_profile$', 'Account.views.view_profile', name="view_profile"),
                       url(r'^change_password$', 'Account.views.change_password', name="change_password"),
                       url(r'^edit_profile$', 'Account.views.edit_profile', name="edit_profile"),
                       url(r'^delete_user$', 'Account.views.delete_user', name="delete_user"),
                       url(r'^create_user$', 'Account.views.create_user', name="create_user"),
                       url(r'^admin_password_change$', 'Account.views.change_user_password',
                           name="change_user_password"),
)
