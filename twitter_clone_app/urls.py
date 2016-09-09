from django.conf.urls import url

from . import views


app_name = 'twitter_clone_app'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^help/$', views.help, name='help'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^signup$', views.sign_up, name='sign-up'),

    # /users/<pk>/
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserProfileView.as_view(),
        name='user-profile')
]
