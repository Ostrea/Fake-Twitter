from django.conf.urls import url

from . import views


app_name = 'twitter_clone_app'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^help/$', views.help, name='help'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),

    # Auth urls
    url(r'^signup/$', views.sign_up, name='sign-up'),
    url(r'^create-user/$', views.create_user, name='create-user'),
    url(r'^login/$', views.log_in, name='log-in'),
    url(r'^logout/$', views.log_out, name='log-out'),

    # Users urls.
    # /users/<user_id>/
    url(r'^users/(?P<user_id>[0-9]+)/$', views.user_profile,
        name='user-profile'),
    url(r'^users/all/$', views.show_all_users, name='show-all-users'),

    url(r'^edit/$', views.edit_user, name='edit-user')
]
