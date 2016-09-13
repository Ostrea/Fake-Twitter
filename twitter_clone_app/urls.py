from django.conf.urls import url

from . import views


app_name = 'twitter_clone_app'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^help/$', views.help, name='help'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^signup$', views.sign_up, name='sign-up'),
    url(r'^create-user$', views.create_user, name='create-user'),

    # /users/<user_id>/
    url(r'^users/(?P<user_id>[0-9]+)/$', views.user_profile,
        name='user-profile')
]
